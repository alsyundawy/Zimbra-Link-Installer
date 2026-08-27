#!/usr/bin/env bash
# ==============================================================================
# ZIMBRA LINK INSTALLER & TELEMETRY SUITE
# Enterprise Binary Downloader, Checksum Verifier & Automated Installer (ZCS 7-10.1)
#
# Author    : Harry Dertin Sutisna Alsyundawy
# License   : MIT License
# GitHub    : https://github.com/alsyundawy/Zimbra-Link-Installer
# ==============================================================================

set -Eeuo pipefail

# ANSI Color Definitions
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly CYAN='\033[0;36m'
readonly BOLD='\033[1m'
readonly NC='\033[0m'

# Global Defaults
WORK_DIR="${HOME}/zimbra_install_cache"
DEFAULT_REFERER="https://techfiles.online/"

log_info() {
	printf "%b[*] %s%b\n" "${CYAN}" "$1" "${NC}"
}

log_success() {
	printf "%b[+] %s%b\n" "${GREEN}" "$1" "${NC}"
}

log_warn() {
	printf "%b[!] %s%b\n" "${YELLOW}" "$1" "${NC}"
}

log_error() {
	printf "%b[x] %s%b\n" "${RED}" "$1" "${NC}" >&2
}

banner() {
	clear 2>/dev/null || true
	printf "%b%b" "${CYAN}" "${BOLD}"
	cat <<'BANNER_EOF'
  ====================================================================
               Z I M B R A   L I N K   I N S T A L L E R
          Enterprise Binary Downloader & Automated Suite (v2.0.0)
  ====================================================================
BANNER_EOF
	printf "%b" "${NC}"
	printf "  Maintained by Harry Dertin Sutisna Alsyundawy (%balsyundawy@gmail.com%b)\n" "${CYAN}" "${NC}"
	printf "====================================================================\n\n"
}

# OS & Architecture Detection
detect_os() {
	ARCH=$(uname -m)
	if [[ ${ARCH} != "x86_64" ]]; then
		log_error "Architecture '${ARCH}' is not supported by standard Zimbra binaries (x86_64 required)."
		exit 1
	fi

	if [[ -f /etc/os-release ]]; then
		# shellcheck disable=SC1091
		. /etc/os-release
		OS_ID="${ID}"
		OS_VER="${VERSION_ID:-}"
		OS_NAME="${PRETTY_NAME:-Linux}"
	else
		log_error "Cannot determine Linux distribution (/etc/os-release missing)."
		exit 1
	fi

	log_success "Detected Architecture : ${ARCH}"
	log_success "Detected Distribution : ${OS_NAME} (${OS_ID} ${OS_VER})"
}

# Pre-flight Check
preflight_check() {
	printf "\n%b--- [1/3] Memeriksa Kesiapan Sistem (Pre-Flight Checks) ---%b\n" "${BOLD}" "${NC}"

	# 1. RAM Check
	if [[ -f /proc/meminfo ]]; then
		TOTAL_RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
		TOTAL_RAM_GB=$((TOTAL_RAM_KB / 1024 / 1024))
		if ((TOTAL_RAM_GB < 8)); then
			log_warn "RAM Terdeteksi: ${TOTAL_RAM_GB} GB (Zimbra merekomendasikan minimal 8 GB RAM, ideal 16+ GB)."
		else
			log_success "RAM Terdeteksi: ${TOTAL_RAM_GB} GB (Memenuhi syarat minimum)."
		fi
	fi

	# 2. Disk Space Check
	FREE_DISK_GB=$(df -BG /opt 2>/dev/null | awk 'NR==2 {print $4}' | sed 's/G//' || df -BG / | awk 'NR==2 {print $4}' | sed 's/G//')
	if ((FREE_DISK_GB < 30)); then
		log_warn "Ruang Disk Kosong: ${FREE_DISK_GB} GB (Direkomendasikan minimal 50 GB kosong untuk /opt/zimbra)."
	else
		log_success "Ruang Disk Kosong: ${FREE_DISK_GB} GB (Cukup untuk instalasi)."
	fi

	# 3. Check Required Packages
	local missing_pkgs=()
	if [[ ${OS_ID} =~ ^(ubuntu|debian)$ ]]; then
		for pkg in wget curl tar pax sysstat net-tools; do
			if ! dpkg -s "${pkg}" >/dev/null 2>&1; then
				missing_pkgs+=("${pkg}")
			fi
		done
		if [[ ${#missing_pkgs[@]} -gt 0 ]]; then
			log_warn "Paket pendukung belum lengkap: ${missing_pkgs[*]}"
			read -rp "Install dependensi pendukung sekarang via apt? [Y/n]: " do_install
			if [[ ${do_install:-Y} =~ ^[Yy]$ ]]; then
				sudo apt-get update && sudo apt-get install -y "${missing_pkgs[@]}"
			fi
		else
			log_success "Seluruh paket sistem wajib (pax, sysstat, net-tools) telah terpasang."
		fi
	elif [[ ${OS_ID} =~ ^(rhel|rocky|almalinux|centos)$ ]]; then
		for pkg in wget curl tar pax sysstat net-tools; do
			if ! rpm -q "${pkg}" >/dev/null 2>&1; then
				missing_pkgs+=("${pkg}")
			fi
		done
		if [[ ${#missing_pkgs[@]} -gt 0 ]]; then
			log_warn "Paket pendukung belum lengkap: ${missing_pkgs[*]}"
			read -rp "Install dependensi pendukung sekarang via dnf/yum? [Y/n]: " do_install
			if [[ ${do_install:-Y} =~ ^[Yy]$ ]]; then
				sudo dnf install -y "${missing_pkgs[@]}" || sudo yum install -y "${missing_pkgs[@]}"
			fi
		else
			log_success "Seluruh paket sistem wajib telah terpasang."
		fi
	fi
}

# Download & Checksum Helper
download_and_verify() {
	local tgz_url="$1"
	local sha_url="${2:-}"
	local is_referer_req="${3:-false}"

	mkdir -p "${WORK_DIR}"
	cd "${WORK_DIR}"

	local file_name
	file_name=$(basename "${tgz_url}")

	printf "\n%b--- [2/3] Mengunduh Biner Zimbra ---%b\n" "${BOLD}" "${NC}"
	log_info "Target File : ${file_name}"
	log_info "Sumber URL  : ${tgz_url}"

	local curl_opts=("-L" "-C" "-" "--progress-bar" "-o" "${file_name}")
	if [[ ${is_referer_req} == "true" ]]; then
		curl_opts+=("-H" "Referer: ${DEFAULT_REFERER}")
	fi

	if [[ -f ${file_name} ]]; then
		log_warn "Berkas ${file_name} sudah ada di ${WORK_DIR}. Memeriksa resume/keutuhan berkas..."
	fi

	curl "${curl_opts[@]}" "${tgz_url}"
	log_success "Unduhan biner selesai: ${file_name}"

	# Checksum Verification
	if [[ -n ${sha_url} ]]; then
		printf "\n%b--- [3/3] Verifikasi Integritas Kriptografi ---%b\n" "${BOLD}" "${NC}"
		local sha_file
		sha_file=$(basename "${sha_url}")
		log_info "Mengunduh berkas checksum: ${sha_file}"

		local sha_opts=("-sL" "-o" "${sha_file}")
		if [[ ${is_referer_req} == "true" ]]; then
			sha_opts+=("-H" "Referer: ${DEFAULT_REFERER}")
		fi
		curl "${sha_opts[@]}" "${sha_url}"

		if [[ ${sha_file} == *.sha256 ]]; then
			local expected_hash
			expected_hash=$(awk '{print $1}' "${sha_file}")
			local actual_hash
			actual_hash=$(sha256sum "${file_name}" | awk '{print $1}')
			log_info "Expected SHA256: ${expected_hash}"
			log_info "Actual   SHA256: ${actual_hash}"
			if [[ ${expected_hash} == "${actual_hash}" ]]; then
				log_success "VERIFIKASI SHA256 VALID: Integritas biner terjamin 100%!"
			else
				log_error "HASH MISMATCH: Berkas rusak atau korup saat diunduh!"
				exit 1
			fi
		elif [[ ${sha_file} == *.md5 ]]; then
			local expected_hash
			expected_hash=$(awk '{print $1}' "${sha_file}")
			local actual_hash
			actual_hash=$(md5sum "${file_name}" | awk '{print $1}')
			log_info "Expected MD5: ${expected_hash}"
			log_info "Actual   MD5: ${actual_hash}"
			if [[ ${expected_hash} == "${actual_hash}" ]]; then
				log_success "VERIFIKASI MD5 VALID: Integritas biner terjamin 100%!"
			else
				log_error "MD5 MISMATCH: Berkas rusak atau korup!"
				exit 1
			fi
		fi
	fi

	printf "\n"
	read -rp "Apakah Anda ingin mengekstrak arsip dan memulai instalasi ZCS sekarang? [y/N]: " do_run_install
	if [[ ${do_run_install:-N} =~ ^[Yy]$ ]]; then
		log_info "Mengekstrak ${file_name}..."
		tar -xzvf "${file_name}"
		local extracted_dir
		extracted_dir="${file_name%.tgz}"
		if [[ -d ${extracted_dir} ]]; then
			cd "${extracted_dir}"
			log_success "Masuk ke direktori: $(pwd)"
			log_info "Menjalankan ./install.sh dengan izin sudo..."
			sudo ./install.sh
		else
			log_warn "Direktori ekstraksi tidak standar. Silakan cek di: ${WORK_DIR}"
		fi
	else
		log_info "Biner tersimpan di: ${WORK_DIR}/${file_name}"
		log_info "Untuk menginstal nanti, jalankan:"
		printf "  cd %s\n" "${WORK_DIR}"
		printf "  tar -xzvf %s\n" "${file_name}"
		printf "  cd %s && sudo ./install.sh\n\n" "${file_name%.tgz}"
	fi
}

menu_techfiles_10_1() {
	printf "\n%b=== Pilihan Zimbra FOSS 10.1.20 (TechFiles / Ian Walker) ===%b\n" "${BOLD}" "${NC}"
	printf "  1) Ubuntu 24.04 LTS (Noble Numbat)\n"
	printf "  2) Ubuntu 22.04 LTS (Jammy Jellyfish)\n"
	printf "  3) RHEL 9 / Rocky 9 / Alma 9 / Oracle 9\n"
	printf "  4) RHEL 8 / Rocky 8 / Alma 8 / Oracle 8\n"
	printf "  0) Kembali ke Menu Utama\n"
	read -rp "Pilih OS Target [1-4]: " sub_choice
	case "${sub_choice}" in
	1)
		download_and_verify \
			"https://cdn.techfiles.online/ubuntu/zcs-10.1.20_GA_0326.UBUNTU24_64.20260821120929.tgz" \
			"https://cdn.techfiles.online/ubuntu/zcs-10.1.20_GA_0326.UBUNTU24_64.20260821120929.tgz.sha256" \
			"true"
		;;
	2)
		download_and_verify \
			"https://cdn.techfiles.online/ubuntu/zcs-10.1.20_GA_0326.UBUNTU22_64.20260821115118.tgz" \
			"https://cdn.techfiles.online/ubuntu/zcs-10.1.20_GA_0326.UBUNTU22_64.20260821115118.tgz.sha256" \
			"true"
		;;
	3)
		download_and_verify \
			"https://cdn.techfiles.online/rhel/zcs-10.1.20_GA_0326.RHEL9_64.20260821135258.tgz" \
			"https://cdn.techfiles.online/rhel/zcs-10.1.20_GA_0326.RHEL9_64.20260821135258.tgz.sha256" \
			"true"
		;;
	4)
		download_and_verify \
			"https://cdn.techfiles.online/rhel/zcs-10.1.20_GA_0326.RHEL8_64.20260821135029.tgz" \
			"https://cdn.techfiles.online/rhel/zcs-10.1.20_GA_0326.RHEL8_64.20260821135029.tgz.sha256" \
			"true"
		;;
	*)
		return
		;;
	esac
}

menu_maldua_10_1() {
	printf "\n%b=== Pilihan Zimbra FOSS 10.1.20.p1 (Maldua Releases) ===%b\n" "${BOLD}" "${NC}"
	printf "  1) Ubuntu 24.04 LTS\n"
	printf "  2) Ubuntu 22.04 LTS\n"
	printf "  3) Ubuntu 20.04 LTS\n"
	printf "  4) RHEL 9 / Rocky 9 / Alma 9\n"
	printf "  5) RHEL 8 / Rocky 8 / Alma 8\n"
	printf "  0) Kembali\n"
	read -rp "Pilih OS Target [1-5]: " sub_choice
	case "${sub_choice}" in
	1)
		download_and_verify \
			"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-ubuntu-24.04/zcs-10.1.20_GA_0326.UBUNTU24_64.20260821120929.tgz" \
			"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-ubuntu-24.04/zcs-10.1.20_GA_0326.UBUNTU24_64.20260821120929.tgz.sha256" \
			"false"
		;;
	2)
		download_and_verify \
			"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-ubuntu-22.04/zcs-10.1.20_GA_0326.UBUNTU22_64.20260821115118.tgz" \
			"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-ubuntu-22.04/zcs-10.1.20_GA_0326.UBUNTU22_64.20260821115118.tgz.sha256" \
			"false"
		;;
	3)
		download_and_verify \
			"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-ubuntu-20.04/zcs-10.1.20_GA_0326.UBUNTU20_64.20260821124614.tgz" \
			"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-ubuntu-20.04/zcs-10.1.20_GA_0326.UBUNTU20_64.20260821124614.tgz.sha256" \
			"false"
		;;
	4)
		download_and_verify \
			"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-rhel-9/zcs-10.1.20_GA_0326.RHEL9_64.20260821135258.tgz" \
			"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-rhel-9/zcs-10.1.20_GA_0326.RHEL9_64.20260821135258.tgz.sha256" \
			"false"
		;;
	5)
		download_and_verify \
			"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-rhel-8/zcs-10.1.20_GA_0326.RHEL8_64.20260821135029.tgz" \
			"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-rhel-8/zcs-10.1.20_GA_0326.RHEL8_64.20260821135029.tgz.sha256" \
			"false"
		;;
	*)
		return
		;;
	esac
}

menu_official_ne() {
	printf "\n%b=== Pilihan Zimbra Network Edition (Official Synacor) ===%b\n" "${BOLD}" "${NC}"
	printf "  1) ZCS NE 10.1.0 GA (Ubuntu 22.04 LTS)\n"
	printf "  0) Kembali\n"
	read -rp "Pilih Versi [1]: " sub_choice
	case "${sub_choice}" in
	1)
		download_and_verify \
			"https://files.zimbra.com/downloads/10.1.0_GA/zcs-NETWORK-10.1.0_GA_4655.UBUNTU22_64.20240819064312.tgz" \
			"https://files.zimbra.com/downloads/10.1.0_GA/zcs-NETWORK-10.1.0_GA_4655.UBUNTU22_64.20240819064312.tgz.sha256" \
			"false"
		;;
	*)
		return
		;;
	esac
}

menu_legacy_lts() {
	printf "\n%b=== Pilihan Zimbra Legacy LTS Official (files.zimbra.com) ===%b\n" "${BOLD}" "${NC}"
	printf "  1) ZCS 8.8.15 GA 4179 (Ubuntu 20.04 LTS)\n"
	printf "  2) ZCS 8.8.15 GA 3953 (RHEL 8 / Rocky 8)\n"
	printf "  3) ZCS 8.6.0 GA 1153 (Ubuntu 14.04 LTS)\n"
	printf "  4) ZCS 8.6.0 GA 1153 (RHEL 7 / CentOS 7)\n"
	printf "  5) ZCS 8.0.9 GA 6191 (Ubuntu 12.04 LTS)\n"
	printf "  0) Kembali\n"
	read -rp "Pilih Versi [1-5]: " sub_choice
	case "${sub_choice}" in
	1)
		download_and_verify \
			"https://files.zimbra.com/downloads/8.8.15_GA/zcs-8.8.15_GA_4179.UBUNTU20_64.20211118033954.tgz" \
			"" "false"
		;;
	2)
		download_and_verify \
			"https://files.zimbra.com/downloads/8.8.15_GA/zcs-8.8.15_GA_3953.RHEL8_64.20200629025823.tgz" \
			"" "false"
		;;
	3)
		download_and_verify \
			"https://files.zimbra.com/downloads/8.6.0_GA/zcs-8.6.0_GA_1153.UBUNTU14_64.20141215151116.tgz" \
			"" "false"
		;;
	4)
		download_and_verify \
			"https://files.zimbra.com/downloads/8.6.0_GA/zcs-8.6.0_GA_1153.RHEL7_64.20141215151110.tgz" \
			"" "false"
		;;
	5)
		download_and_verify \
			"https://files.zimbra.com/downloads/8.0.9_GA/zcs-8.0.9_GA_6191.UBUNTU12_64.20141103151539.tgz" \
			"" "false"
		;;
	*)
		return
		;;
	esac
}

main_menu() {
	while true; do
		banner
		detect_os
		printf "\n%bPilih Kategori Biner Zimbra:%b\n" "${BOLD}" "${NC}"
		printf "  1) Zimbra FOSS 10.1.20 (TechFiles / Ian Walker Builds - Latest)\n"
		printf "  2) Zimbra FOSS 10.1.x (Maldua Community Releases)\n"
		printf "  3) Zimbra Network Edition 10.1.0 GA (Official Synacor)\n"
		printf "  4) Zimbra Legacy Official LTS (8.8.15, 8.6.0, 8.0.9)\n"
		printf "  5) Jalankan Pre-Flight System Audit & Prerequisite Check\n"
		printf "  6) Jalankan Uji Telemetri Seluruh Link Biner (Deep Link Validator)\n"
		printf "  0) Keluar\n"
		printf "====================================================================\n"
		read -rp "Masukkan Pilihan Anda [0-6]: " main_choice

		case "${main_choice}" in
		1) menu_techfiles_10_1 ;;
		2) menu_maldua_10_1 ;;
		3) menu_official_ne ;;
		4) menu_legacy_lts ;;
		5)
			preflight_check
			read -rp "Tekan Enter untuk kembali ke menu..."
			;;
		6)
			if command -v python3 >/dev/null 2>&1 && [[ -f scripts/deep_link_validator.py ]]; then
				python3 scripts/deep_link_validator.py
			else
				log_warn "Python3 atau skrip validator tidak ditemukan."
			fi
			read -rp "Tekan Enter untuk kembali ke menu..."
			;;
		0)
			printf "\nTerima kasih telah menggunakan Zimbra Link Installer!\n"
			exit 0
			;;
		*)
			log_error "Pilihan tidak valid."
			sleep 1
			;;
		esac
	done
}

# Entrypoint
if [[ ${BASH_SOURCE[0]} == "${0}" ]]; then
	main_menu "$@"
fi
