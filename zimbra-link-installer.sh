#!/usr/bin/env bash
# ==============================================================================
# ZIMBRA LINK INSTALLER & TELEMETRY SUITE (v2.5.0)
# Enterprise Binary Downloader, Checksum Verifier & Automated Installer
# Supports Official NE (7-10.1), Official FOSS (7-8.8), and Community FOSS (8.8-10.1)
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
          Enterprise Binary Downloader & Automated Suite (v2.5.0)
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
	elif [[ ${OS_ID} =~ ^(rhel|rocky|almalinux|centos|ol)$ ]]; then
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
	local checksum_url="${2:-}"
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
	if [[ -n ${checksum_url} ]]; then
		printf "\n%b--- [3/3] Verifikasi Integritas Kriptografi ---%b\n" "${BOLD}" "${NC}"
		local chk_file
		chk_file=$(basename "${checksum_url}")
		log_info "Mengunduh berkas checksum: ${chk_file}"

		local chk_opts=("-sL" "-o" "${chk_file}")
		if [[ ${is_referer_req} == "true" ]]; then
			chk_opts+=("-H" "Referer: ${DEFAULT_REFERER}")
		fi
		curl "${chk_opts[@]}" "${checksum_url}"

		if [[ ${chk_file} == *.sha256 ]]; then
			local expected_hash
			expected_hash=$(awk '{print $1}' "${chk_file}")
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
		elif [[ ${chk_file} == *.md5 ]]; then
			local expected_hash
			expected_hash=$(awk '{print $1}' "${chk_file}")
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

# ==============================================================================
# MENU 1: OFFICIAL NETWORK EDITION (NE)
# ==============================================================================
menu_official_ne() {
	while true; do
		printf "\n%b=== OFFICIAL ZIMBRA NETWORK EDITION (files.zimbra.com) ===%b\n" "${BOLD}" "${NC}"
		printf "  1) ZCS NE 10.1.0 GA (Ubuntu 22.04 LTS / RHEL 9)\n"
		printf "  2) ZCS NE 10.0.0 GA (Ubuntu 20.04 / Ubuntu 18.04 / RHEL 7)\n"
		printf "  3) ZCS NE 9.0.0 GA (Ubuntu 20.04 / Ubuntu 18.04 / RHEL 8 / RHEL 7)\n"
		printf "  4) ZCS NE 8.8.15 GA (Ubuntu 20.04 / Ubuntu 18.04 / RHEL 8 / RHEL 7)\n"
		printf "  5) ZCS NE 8.8.11 / 8.8.9 / 8.8.8 / 8.8.7 GA (RHEL 6/7, Ubuntu 14/16)\n"
		printf "  6) ZCS NE 8.7.1 GA / 8.7.0 GA (Ubuntu 16/14/12, RHEL 7/6)\n"
		printf "  7) ZCS NE 8.6.0 GA / 8.5.1 / 8.5.0 / 8.0.9 / 7.2.7 GA (Legacy Official)\n"
		printf "  0) Kembali ke Menu Utama\n"
		read -rp "Pilih Versi NE [0-7]: " ne_choice

		case "${ne_choice}" in
		1)
			printf "\n%b[ZCS NE 10.1.0 GA]%b\n" "${CYAN}" "${NC}"
			printf "  1) Ubuntu 22.04 LTS (x86_64)\n"
			printf "  2) RHEL / Rocky / Alma 9 (x86_64)\n"
			read -rp "Pilih OS: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/10.1.0_GA/zcs-NETWORK-10.1.0_GA_4655.UBUNTU22_64.20240819064312.tgz" \
					"https://files.zimbra.com/downloads/10.1.0_GA/zcs-NETWORK-10.1.0_GA_4655.UBUNTU22_64.20240819064312.tgz.sha256" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/10.1.0_GA/zcs-NETWORK-10.1.0_GA_4688.RHEL9_64.20240911074203.tgz" \
					"https://files.zimbra.com/downloads/10.1.0_GA/zcs-NETWORK-10.1.0_GA_4688.RHEL9_64.20240911074203.tgz.sha256" "false"
			fi
			;;
		2)
			printf "\n%b[ZCS NE 10.0.0 GA]%b\n" "${CYAN}" "${NC}"
			printf "  1) Ubuntu 20.04 LTS (x86_64)\n"
			printf "  2) Ubuntu 18.04 LTS (x86_64)\n"
			printf "  3) RHEL 7 / CentOS 7 (x86_64)\n"
			read -rp "Pilih OS: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/10.0.0_GA/zcs-NETWORK-10.0.0_GA_4518.UBUNTU20_64.20230301065514.tgz" \
					"https://files.zimbra.com/downloads/10.0.0_GA/zcs-NETWORK-10.0.0_GA_4518.UBUNTU20_64.20230301065514.tgz.md5" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/10.0.0_GA/zcs-NETWORK-10.0.0_GA_4518.UBUNTU18_64.20230301065514.tgz" \
					"https://files.zimbra.com/downloads/10.0.0_GA/zcs-NETWORK-10.0.0_GA_4518.UBUNTU18_64.20230301065514.tgz.sha256" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/10.0.0_GA/zcs-NETWORK-10.0.0_GA_4518.RHEL7_64.20230301065514.tgz" \
					"https://files.zimbra.com/downloads/10.0.0_GA/zcs-NETWORK-10.0.0_GA_4518.RHEL7_64.20230301065514.tgz.md5" "false"
			fi
			;;
		3)
			printf "\n%b[ZCS NE 9.0.0 GA Kepler]%b\n" "${CYAN}" "${NC}"
			printf "  1) Ubuntu 20.04 LTS (x86_64)\n"
			printf "  2) Ubuntu 18.04 LTS (x86_64)\n"
			printf "  3) RHEL 8 / Rocky 8 (x86_64)\n"
			printf "  4) RHEL 7 / CentOS 7 (x86_64)\n"
			read -rp "Pilih OS: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/9.0.0_GA/zcs-NETWORK-9.0.0_GA_3954.UBUNTU20_64.20200629025823.tgz" \
					"https://files.zimbra.com/downloads/9.0.0_GA/zcs-NETWORK-9.0.0_GA_3954.UBUNTU20_64.20200629025823.tgz.sha256" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/9.0.0_GA/zcs-NETWORK-9.0.0_GA_3924.UBUNTU18_64.20200408143213.tgz" \
					"https://files.zimbra.com/downloads/9.0.0_GA/zcs-NETWORK-9.0.0_GA_3924.UBUNTU18_64.20200408143213.tgz.sha256" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/9.0.0_GA/zcs-NETWORK-9.0.0_GA_3954.RHEL8_64.20200629025823.tgz" \
					"https://files.zimbra.com/downloads/9.0.0_GA/zcs-NETWORK-9.0.0_GA_3954.RHEL8_64.20200629025823.tgz.sha256" "false"
			elif [[ ${os_c} == "4" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/9.0.0_GA/zcs-NETWORK-9.0.0_GA_3924.RHEL7_64.20200408143213.tgz" \
					"https://files.zimbra.com/downloads/9.0.0_GA/zcs-NETWORK-9.0.0_GA_3924.RHEL7_64.20200408143213.tgz.sha256" "false"
			fi
			;;
		4)
			printf "\n%b[ZCS NE 8.8.15 GA Joule]%b\n" "${CYAN}" "${NC}"
			printf "  1) Ubuntu 20.04 LTS (Build 3953)\n"
			printf "  2) Ubuntu 18.04 LTS (Build 3869)\n"
			printf "  3) RHEL 8 / Rocky 8 (Build 3953)\n"
			printf "  4) RHEL 7 / CentOS 7 (Build 3869)\n"
			read -rp "Pilih OS: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.15_GA/zcs-NETWORK-8.8.15_GA_3953.UBUNTU20_64.20200629025823.tgz" \
					"https://files.zimbra.com/downloads/8.8.15_GA/zcs-NETWORK-8.8.15_GA_3953.UBUNTU20_64.20200629025823.tgz.sha256" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.15_GA/zcs-NETWORK-8.8.15_GA_3869.UBUNTU18_64.20190918004220.tgz" \
					"https://files.zimbra.com/downloads/8.8.15_GA/zcs-NETWORK-8.8.15_GA_3869.UBUNTU18_64.20190918004220.tgz.sha256" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.15_GA/zcs-NETWORK-8.8.15_GA_3953.RHEL8_64.20200629025823.tgz" \
					"https://files.zimbra.com/downloads/8.8.15_GA/zcs-NETWORK-8.8.15_GA_3953.RHEL8_64.20200629025823.tgz.sha256" "false"
			elif [[ ${os_c} == "4" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.15_GA/zcs-NETWORK-8.8.15_GA_3869.RHEL7_64.20190918004220.tgz" \
					"https://files.zimbra.com/downloads/8.8.15_GA/zcs-NETWORK-8.8.15_GA_3869.RHEL7_64.20190918004220.tgz.sha256" "false"
			fi
			;;
		5)
			printf "\n%b[ZCS NE 8.8.11 / 8.8.9 / 8.8.8 / 8.8.7 GA]%b\n" "${CYAN}" "${NC}"
			printf "  1) NE 8.8.11 GA (Ubuntu 16.04)\n"
			printf "  2) NE 8.8.11 GA (RHEL 7 / CentOS 7)\n"
			printf "  3) NE 8.8.9 GA (Ubuntu 16.04)\n"
			printf "  4) NE 8.8.9 GA (RHEL 7)\n"
			read -rp "Pilih Versi: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.11_GA/zcs-NETWORK-8.8.11_GA_3737.UBUNTU16_64.20181207111719.tgz" \
					"https://files.zimbra.com/downloads/8.8.11_GA/zcs-NETWORK-8.8.11_GA_3737.UBUNTU16_64.20181207111719.tgz.sha256" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.11_GA/zcs-NETWORK-8.8.11_GA_3737.RHEL7_64.20181207111719.tgz" \
					"https://files.zimbra.com/downloads/8.8.11_GA/zcs-NETWORK-8.8.11_GA_3737.RHEL7_64.20181207111719.tgz.sha256" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.9_GA/zcs-NETWORK-8.8.9_GA_3019.UBUNTU16_64.20180809160254.tgz" \
					"https://files.zimbra.com/downloads/8.8.9_GA/zcs-NETWORK-8.8.9_GA_3019.UBUNTU16_64.20180809160254.tgz.sha256" "false"
			elif [[ ${os_c} == "4" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.9_GA/zcs-NETWORK-8.8.9_GA_3019.RHEL7_64.20180809160254.tgz" \
					"https://files.zimbra.com/downloads/8.8.9_GA/zcs-NETWORK-8.8.9_GA_3019.RHEL7_64.20180809160254.tgz.sha256" "false"
			fi
			;;
		6)
			printf "\n%b[ZCS NE 8.7.1 GA & 8.7.0 GA]%b\n" "${CYAN}" "${NC}"
			printf "  1) NE 8.7.1 GA (Ubuntu 16.04 LTS)\n"
			printf "  2) NE 8.7.1 GA (Ubuntu 14.04 LTS)\n"
			printf "  3) NE 8.7.1 GA (RHEL 7 / CentOS 7)\n"
			printf "  4) NE 8.7.1 GA (RHEL 6 / CentOS 6)\n"
			printf "  5) NE 8.7.0 GA (Ubuntu 16.04 LTS)\n"
			printf "  6) NE 8.7.0 GA (RHEL 7)\n"
			read -rp "Pilih Versi: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-NETWORK-8.7.1_GA_1670.UBUNTU16_64.20161025045209.tgz" \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-NETWORK-8.7.1_GA_1670.UBUNTU16_64.20161025045209.tgz.sha256" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-NETWORK-8.7.1_GA_1670.UBUNTU14_64.20161025045142.tgz" \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-NETWORK-8.7.1_GA_1670.UBUNTU14_64.20161025045142.tgz.sha256" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-NETWORK-8.7.1_GA_1670.RHEL7_64.20161025045328.tgz" \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-NETWORK-8.7.1_GA_1670.RHEL7_64.20161025045328.tgz.sha256" "false"
			elif [[ ${os_c} == "4" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-NETWORK-8.7.1_GA_1670.RHEL6_64.20161025035121.tgz" \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-NETWORK-8.7.1_GA_1670.RHEL6_64.20161025035121.tgz.sha256" "false"
			elif [[ ${os_c} == "5" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.7.0_GA/zcs-NETWORK-8.7.0_GA_1659.UBUNTU16_64.20160628202702.tgz" \
					"https://files.zimbra.com/downloads/8.7.0_GA/zcs-NETWORK-8.7.0_GA_1659.UBUNTU16_64.20160628202702.tgz.sha256" "false"
			elif [[ ${os_c} == "6" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.7.0_GA/zcs-NETWORK-8.7.0_GA_1659.RHEL7_64.20160628202904.tgz" \
					"https://files.zimbra.com/downloads/8.7.0_GA/zcs-NETWORK-8.7.0_GA_1659.RHEL7_64.20160628202904.tgz.sha256" "false"
			fi
			;;
		7)
			printf "\n%b[ZCS NE Legacy: 8.6.0 / 8.5.1 / 8.0.9 / 7.2.7]%b\n" "${CYAN}" "${NC}"
			printf "  1) NE 8.6.0 GA (Ubuntu 14.04 LTS)\n"
			printf "  2) NE 8.6.0 GA (RHEL 6 / CentOS 6)\n"
			printf "  3) NE 8.5.1 GA (Ubuntu 14.04 LTS)\n"
			printf "  4) NE 8.0.9 GA (Ubuntu 12.04 LTS)\n"
			printf "  5) NE 7.2.7 GA (Ubuntu 10.04 LTS)\n"
			read -rp "Pilih Versi: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.6.0_GA/zcs-NETWORK-8.6.0_GA_1153.UBUNTU14_64.20141215151218.tgz" \
					"https://files.zimbra.com/downloads/8.6.0_GA/zcs-NETWORK-8.6.0_GA_1153.UBUNTU14_64.20141215151218.tgz.sha256" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.6.0_GA/zcs-NETWORK-8.6.0_GA_1153.RHEL6_64.20141215151258.tgz" \
					"https://files.zimbra.com/downloads/8.6.0_GA/zcs-NETWORK-8.6.0_GA_1153.RHEL6_64.20141215151258.tgz.sha256" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.5.1_GA/zcs-NETWORK-8.5.1_GA_3056.UBUNTU14_64.20141103151651.tgz" \
					"https://files.zimbra.com/downloads/8.5.1_GA/zcs-NETWORK-8.5.1_GA_3056.UBUNTU14_64.20141103151651.tgz.sha256" "false"
			elif [[ ${os_c} == "4" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.0.9_GA/zcs-NETWORK-8.0.9_GA_6191.UBUNTU12_64.20141103151656.tgz" \
					"https://files.zimbra.com/downloads/8.0.9_GA/zcs-NETWORK-8.0.9_GA_6191.UBUNTU12_64.20141103151656.tgz.sha256" "false"
			elif [[ ${os_c} == "5" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/7.2.7_GA/zcs-NETWORK-7.2.7_GA_2942.UBUNTU10_64.20140314190301.tgz" \
					"https://files.zimbra.com/downloads/7.2.7_GA/zcs-NETWORK-7.2.7_GA_2942.UBUNTU10_64.20140314190301.tgz.md5" "false"
			fi
			;;
		0)
			return
			;;
		*)
			log_error "Pilihan tidak valid."
			;;
		esac
	done
}

# ==============================================================================
# MENU 2: OFFICIAL OPEN SOURCE EDITION (FOSS / OSE)
# ==============================================================================
menu_official_foss() {
	while true; do
		printf "\n%b=== OFFICIAL ZIMBRA OPEN SOURCE EDITION (FOSS / OSE) ===%b\n" "${BOLD}" "${NC}"
		printf "  1) ZCS FOSS 8.8.15 GA (Ubuntu 20.04, Ubuntu 18.04, RHEL 8, RHEL 7)\n"
		printf "  2) ZCS FOSS 8.8.11 / 8.8.9 / 8.8.8 / 8.8.7 GA (Ubuntu 16/14, RHEL 7/6)\n"
		printf "  3) ZCS FOSS 8.7.1 GA / 8.7.0 GA (Ubuntu 16/14/12, RHEL 7/6)\n"
		printf "  4) ZCS FOSS 8.6.0 GA / 8.5.1 / 8.5.0 / 8.0.9 / 7.2.7 GA (Legacy Official)\n"
		printf "  0) Kembali ke Menu Utama\n"
		read -rp "Pilih Versi FOSS [0-4]: " foss_choice

		case "${foss_choice}" in
		1)
			printf "\n%b[ZCS FOSS 8.8.15 GA Joule]%b\n" "${CYAN}" "${NC}"
			printf "  1) Ubuntu 20.04 LTS (Build 4179)\n"
			printf "  2) Ubuntu 18.04 LTS (Build 3869)\n"
			printf "  3) RHEL 8 / Rocky 8 (Build 3953)\n"
			printf "  4) RHEL 7 / CentOS 7 (Build 3869)\n"
			read -rp "Pilih OS: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.15_GA/zcs-8.8.15_GA_4179.UBUNTU20_64.20211118033954.tgz" \
					"" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.15_GA/zcs-8.8.15_GA_3869.UBUNTU18_64.20190918004220.tgz" \
					"" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.15_GA/zcs-8.8.15_GA_3953.RHEL8_64.20200629025823.tgz" \
					"" "false"
			elif [[ ${os_c} == "4" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.15_GA/zcs-8.8.15_GA_3869.RHEL7_64.20190918004220.tgz" \
					"" "false"
			fi
			;;
		2)
			printf "\n%b[ZCS FOSS 8.8.11 / 8.8.9 / 8.8.8 / 8.8.7 GA]%b\n" "${CYAN}" "${NC}"
			printf "  1) FOSS 8.8.11 GA (Ubuntu 16.04 LTS)\n"
			printf "  2) FOSS 8.8.11 GA (RHEL 7 / CentOS 7)\n"
			printf "  3) FOSS 8.8.9 GA (Ubuntu 16.04 LTS)\n"
			printf "  4) FOSS 8.8.9 GA (RHEL 7 / CentOS 7)\n"
			printf "  5) FOSS 8.8.8 GA (Ubuntu 16.04 LTS)\n"
			printf "  6) FOSS 8.8.7 GA (Ubuntu 16.04 LTS)\n"
			read -rp "Pilih Versi: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.11_GA/zcs-8.8.11_GA_3737.UBUNTU16_64.20181207111719.tgz" \
					"https://files.zimbra.com/downloads/8.8.11_GA/zcs-8.8.11_GA_3737.UBUNTU16_64.20181207111719.tgz.sha256" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.11_GA/zcs-8.8.11_GA_3737.RHEL7_64.20181207111719.tgz" \
					"https://files.zimbra.com/downloads/8.8.11_GA/zcs-8.8.11_GA_3737.RHEL7_64.20181207111719.tgz.sha256" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.9_GA/zcs-8.8.9_GA_3019.UBUNTU16_64.20180809160254.tgz" \
					"https://files.zimbra.com/downloads/8.8.9_GA/zcs-8.8.9_GA_3019.UBUNTU16_64.20180809160254.tgz.sha256" "false"
			elif [[ ${os_c} == "4" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.9_GA/zcs-8.8.9_GA_3019.RHEL7_64.20180809160254.tgz" \
					"https://files.zimbra.com/downloads/8.8.9_GA/zcs-8.8.9_GA_3019.RHEL7_64.20180809160254.tgz.sha256" "false"
			elif [[ ${os_c} == "5" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.8_GA/zcs-8.8.8_GA_2009.UBUNTU16_64.20180322150747.tgz" \
					"https://files.zimbra.com/downloads/8.8.8_GA/zcs-8.8.8_GA_2009.UBUNTU16_64.20180322150747.tgz.sha256" "false"
			elif [[ ${os_c} == "6" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.8.7_GA/zcs-8.8.7_GA_1964.UBUNTU16_64.20180223145016.tgz" \
					"https://files.zimbra.com/downloads/8.8.7_GA/zcs-8.8.7_GA_1964.UBUNTU16_64.20180223145016.tgz.sha256" "false"
			fi
			;;
		3)
			printf "\n%b[ZCS FOSS 8.7.1 GA & 8.7.0 GA]%b\n" "${CYAN}" "${NC}"
			printf "  1) FOSS 8.7.1 GA (Ubuntu 16.04 LTS)\n"
			printf "  2) FOSS 8.7.1 GA (Ubuntu 14.04 LTS)\n"
			printf "  3) FOSS 8.7.1 GA (RHEL 7 / CentOS 7)\n"
			printf "  4) FOSS 8.7.1 GA (RHEL 6 / CentOS 6)\n"
			printf "  5) FOSS 8.7.0 GA (Ubuntu 16.04 LTS)\n"
			printf "  6) FOSS 8.7.0 GA (RHEL 7)\n"
			read -rp "Pilih Versi: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-8.7.1_GA_1670.UBUNTU16_64.20161025045114.tgz" \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-8.7.1_GA_1670.UBUNTU16_64.20161025045114.tgz.sha256" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-8.7.1_GA_1670.UBUNTU14_64.20161025045105.tgz" \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-8.7.1_GA_1670.UBUNTU14_64.20161025045105.tgz.sha256" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-8.7.1_GA_1670.RHEL7_64.20161025045328.tgz" \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-8.7.1_GA_1670.RHEL7_64.20161025045328.tgz.sha256" "false"
			elif [[ ${os_c} == "4" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-8.7.1_GA_1670.RHEL6_64.20161025035141.tgz" \
					"https://files.zimbra.com/downloads/8.7.1_GA/zcs-8.7.1_GA_1670.RHEL6_64.20161025035141.tgz.sha256" "false"
			elif [[ ${os_c} == "5" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.7.0_GA/zcs-8.7.0_GA_1659.UBUNTU16_64.20160628202554.tgz" \
					"https://files.zimbra.com/downloads/8.7.0_GA/zcs-8.7.0_GA_1659.UBUNTU16_64.20160628202554.tgz.sha256" "false"
			elif [[ ${os_c} == "6" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.7.0_GA/zcs-8.7.0_GA_1659.RHEL7_64.20160628202714.tgz" \
					"https://files.zimbra.com/downloads/8.7.0_GA/zcs-8.7.0_GA_1659.RHEL7_64.20160628202714.tgz.sha256" "false"
			fi
			;;
		4)
			printf "\n%b[ZCS FOSS Legacy: 8.6.0 / 8.5.1 / 8.0.9 / 7.2.7]%b\n" "${CYAN}" "${NC}"
			printf "  1) FOSS 8.6.0 GA (Ubuntu 14.04 LTS)\n"
			printf "  2) FOSS 8.6.0 GA (RHEL 7 / CentOS 7)\n"
			printf "  3) FOSS 8.5.1 GA (Ubuntu 14.04 LTS)\n"
			printf "  4) FOSS 8.0.9 GA (Ubuntu 12.04 LTS)\n"
			printf "  5) FOSS 7.2.7 GA (Ubuntu 10.04 LTS)\n"
			read -rp "Pilih Versi: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.6.0_GA/zcs-8.6.0_GA_1153.UBUNTU14_64.20141215151116.tgz" \
					"https://files.zimbra.com/downloads/8.6.0_GA/zcs-8.6.0_GA_1153.UBUNTU14_64.20141215151116.tgz.sha256" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.6.0_GA/zcs-8.6.0_GA_1153.RHEL7_64.20141215151110.tgz" \
					"https://files.zimbra.com/downloads/8.6.0_GA/zcs-8.6.0_GA_1153.RHEL7_64.20141215151110.tgz.sha256" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.5.1_GA/zcs-8.5.1_GA_3056.UBUNTU14_64.20141103151510.tgz" \
					"https://files.zimbra.com/downloads/8.5.1_GA/zcs-8.5.1_GA_3056.UBUNTU14_64.20141103151510.tgz.sha256" "false"
			elif [[ ${os_c} == "4" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/8.0.9_GA/zcs-8.0.9_GA_6191.UBUNTU12_64.20141103151539.tgz" \
					"https://files.zimbra.com/downloads/8.0.9_GA/zcs-8.0.9_GA_6191.UBUNTU12_64.20141103151539.tgz.sha256" "false"
			elif [[ ${os_c} == "5" ]]; then
				download_and_verify \
					"https://files.zimbra.com/downloads/7.2.7_GA/zcs-7.2.7_GA_2942.UBUNTU10_64.20140314190150.tgz" \
					"https://files.zimbra.com/downloads/7.2.7_GA/zcs-7.2.7_GA_2942.UBUNTU10_64.20140314190150.tgz.md5" "false"
			fi
			;;
		0)
			return
			;;
		*)
			log_error "Pilihan tidak valid."
			;;
		esac
	done
}

# ==============================================================================
# MENU 3: UNOFFICIAL & COMMUNITY FOSS (2018–2026)
# ==============================================================================
menu_community_foss() {
	while true; do
		printf "\n%b=== UNOFFICIAL & COMMUNITY ZCS FOSS ARCHIVE (2018–2026) ===%b\n" "${BOLD}" "${NC}"
		printf "  1) ZCS FOSS 10.1.20 (TechFiles / Ian Walker Builds - Latest)\n"
		printf "  2) ZCS FOSS 10.1.x Series (Maldua Builds - 26 Versions)\n"
		printf "  3) ZCS FOSS 10.0.x Series (Maldua Builds - 17 Versions)\n"
		printf "  4) ZCS FOSS 9.0.0.x Kepler (Maldua Builds - 8 Versions)\n"
		printf "  5) ZCS FOSS 8.8.15.x Joule (Maldua Builds - 8.8.15.p47 / p46)\n"
		printf "  0) Kembali ke Menu Utama\n"
		read -rp "Pilih Kategori Komunitas [0-5]: " comm_choice

		case "${comm_choice}" in
		1)
			printf "\n%b[ZCS FOSS 10.1.20 TechFiles Builds]%b\n" "${CYAN}" "${NC}"
			printf "  1) Ubuntu 24.04 LTS (Noble Numbat)\n"
			printf "  2) Ubuntu 22.04 LTS (Jammy Jellyfish)\n"
			printf "  3) RHEL 9 / Rocky 9 / Alma 9 / Oracle 9\n"
			printf "  4) RHEL 8 / Rocky 8 / Alma 8 / Oracle 8\n"
			read -rp "Pilih OS: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://cdn.techfiles.online/ubuntu/zcs-10.1.20_GA_0326.UBUNTU24_64.20260821120929.tgz" \
					"https://cdn.techfiles.online/ubuntu/zcs-10.1.20_GA_0326.UBUNTU24_64.20260821120929.tgz.sha256" "true"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://cdn.techfiles.online/ubuntu/zcs-10.1.20_GA_0326.UBUNTU22_64.20260821115118.tgz" \
					"https://cdn.techfiles.online/ubuntu/zcs-10.1.20_GA_0326.UBUNTU22_64.20260821115118.tgz.sha256" "true"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://cdn.techfiles.online/rhel/zcs-10.1.20_GA_0326.RHEL9_64.20260821135258.tgz" \
					"https://cdn.techfiles.online/rhel/zcs-10.1.20_GA_0326.RHEL9_64.20260821135258.tgz.sha256" "true"
			elif [[ ${os_c} == "4" ]]; then
				download_and_verify \
					"https://cdn.techfiles.online/rhel/zcs-10.1.20_GA_0326.RHEL8_64.20260821135029.tgz" \
					"https://cdn.techfiles.online/rhel/zcs-10.1.20_GA_0326.RHEL8_64.20260821135029.tgz.sha256" "true"
			fi
			;;
		2)
			printf "\n%b[ZCS FOSS 10.1.20.p1 Maldua Builds]%b\n" "${CYAN}" "${NC}"
			printf "  1) Ubuntu 24.04 LTS\n"
			printf "  2) Ubuntu 22.04 LTS\n"
			printf "  3) Ubuntu 20.04 LTS\n"
			printf "  4) RHEL 9 / Rocky 9 / Alma 9\n"
			printf "  5) RHEL 8 / Rocky 8 / Alma 8\n"
			read -rp "Pilih OS: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-ubuntu-24.04/zcs-10.1.20_GA_0326.UBUNTU24_64.20260821120929.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-ubuntu-24.04/zcs-10.1.20_GA_0326.UBUNTU24_64.20260821120929.tgz.sha256" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-ubuntu-22.04/zcs-10.1.20_GA_0326.UBUNTU22_64.20260821115118.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-ubuntu-22.04/zcs-10.1.20_GA_0326.UBUNTU22_64.20260821115118.tgz.sha256" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-ubuntu-20.04/zcs-10.1.20_GA_0326.UBUNTU20_64.20260821124614.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-ubuntu-20.04/zcs-10.1.20_GA_0326.UBUNTU20_64.20260821124614.tgz.sha256" "false"
			elif [[ ${os_c} == "4" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-rhel-9/zcs-10.1.20_GA_0326.RHEL9_64.20260821135258.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-rhel-9/zcs-10.1.20_GA_0326.RHEL9_64.20260821135258.tgz.sha256" "false"
			elif [[ ${os_c} == "5" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-rhel-8/zcs-10.1.20_GA_0326.RHEL8_64.20260821135029.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/10.1.20.p1-rhel-8/zcs-10.1.20_GA_0326.RHEL8_64.20260821135029.tgz.sha256" "false"
			fi
			;;
		3)
			printf "\n%b[ZCS FOSS 10.0.18.p1 Maldua Builds]%b\n" "${CYAN}" "${NC}"
			printf "  1) Ubuntu 22.04 LTS\n"
			printf "  2) Ubuntu 20.04 LTS\n"
			printf "  3) RHEL 8 / Rocky 8\n"
			read -rp "Pilih OS: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/10.0.18.p1-ubuntu-22.04/zcs-10.0.18_GA_0326.UBUNTU22_64.20260821115118.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/10.0.18.p1-ubuntu-22.04/zcs-10.0.18_GA_0326.UBUNTU22_64.20260821115118.tgz.sha256" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/10.0.18.p1-ubuntu-20.04/zcs-10.0.18_GA_0326.UBUNTU20_64.20260821124614.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/10.0.18.p1-ubuntu-20.04/zcs-10.0.18_GA_0326.UBUNTU20_64.20260821124614.tgz.sha256" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/10.0.18.p1-rhel-8/zcs-10.0.18_GA_0326.RHEL8_64.20260821135029.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/10.0.18.p1-rhel-8/zcs-10.0.18_GA_0326.RHEL8_64.20260821135029.tgz.sha256" "false"
			fi
			;;
		4)
			printf "\n%b[ZCS FOSS 9.0.0.p46 Kepler Builds]%b\n" "${CYAN}" "${NC}"
			printf "  1) Ubuntu 20.04 LTS\n"
			printf "  2) RHEL 8 / Rocky 8\n"
			printf "  3) RHEL 7 / CentOS 7\n"
			read -rp "Pilih OS: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/9.0.0.p46-ubuntu-20.04/zcs-9.0.0_GA_0326.UBUNTU20_64.20260821124614.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/9.0.0.p46-ubuntu-20.04/zcs-9.0.0_GA_0326.UBUNTU20_64.20260821124614.tgz.sha256" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/9.0.0.p46-rhel-8/zcs-9.0.0_GA_0326.RHEL8_64.20260821135029.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/9.0.0.p46-rhel-8/zcs-9.0.0_GA_0326.RHEL8_64.20260821135029.tgz.sha256" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/9.0.0.p46-rhel-7/zcs-9.0.0_GA_0326.RHEL7_64.20260821135029.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/9.0.0.p46-rhel-7/zcs-9.0.0_GA_0326.RHEL7_64.20260821135029.tgz.sha256" "false"
			fi
			;;
		5)
			printf "\n%b[ZCS FOSS 8.8.15.p47 Joule Builds]%b\n" "${CYAN}" "${NC}"
			printf "  1) Ubuntu 20.04 LTS\n"
			printf "  2) Ubuntu 18.04 LTS\n"
			printf "  3) RHEL 8 / Rocky 8\n"
			printf "  4) RHEL 7 / CentOS 7\n"
			read -rp "Pilih OS: " os_c
			if [[ ${os_c} == "1" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/8.8.15.p47-ubuntu-20.04/zcs-8.8.15_GA_0326.UBUNTU20_64.20240821124614.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/8.8.15.p47-ubuntu-20.04/zcs-8.8.15_GA_0326.UBUNTU20_64.20240821124614.tgz.sha256" "false"
			elif [[ ${os_c} == "2" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/8.8.15.p47-ubuntu-18.04/zcs-8.8.15_GA_0326.UBUNTU18_64.20240821124614.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/8.8.15.p47-ubuntu-18.04/zcs-8.8.15_GA_0326.UBUNTU18_64.20240821124614.tgz.sha256" "false"
			elif [[ ${os_c} == "3" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/8.8.15.p47-rhel-8/zcs-8.8.15_GA_0326.RHEL8_64.20240821135029.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/8.8.15.p47-rhel-8/zcs-8.8.15_GA_0326.RHEL8_64.20240821135029.tgz.sha256" "false"
			elif [[ ${os_c} == "4" ]]; then
				download_and_verify \
					"https://github.com/maldua/zimbra-foss/releases/download/8.8.15.p47-rhel-7/zcs-8.8.15_GA_0326.RHEL7_64.20240821135029.tgz" \
					"https://github.com/maldua/zimbra-foss/releases/download/8.8.15.p47-rhel-7/zcs-8.8.15_GA_0326.RHEL7_64.20240821135029.tgz.sha256" "false"
			fi
			;;
		0)
			return
			;;
		*)
			log_error "Pilihan tidak valid."
			;;
		esac
	done
}

# ==============================================================================
# MAIN INTERACTIVE LOOP
# ==============================================================================
main_menu() {
	while true; do
		banner
		detect_os
		printf "\n%bPILIH KATEGORI BINER ZIMBRA:%b\n" "${BOLD}" "${NC}"
		printf "  1) Zimbra OFFICIAL Network Edition (NE) [10.1, 10.0, 9.0, 8.8.x, 8.7.x, 8.6, 8.5, 8.0, 7.x]\n"
		printf "  2) Zimbra OFFICIAL Open Source Edition (FOSS/OSE) [8.8.x, 8.7.x, 8.6, 8.5, 8.0, 7.x]\n"
		printf "  3) Zimbra UNOFFICIAL / Community FOSS Builds [10.1.x, 10.0.x, 9.0.0, 8.8.15 (2018–2026)]\n"
		printf "  4) Jalankan Pre-Flight System Audit & Prerequisite Check\n"
		printf "  5) Jalankan Uji Telemetri Seluruh Link Biner (Deep Link Validator)\n"
		printf "  0) Keluar\n"
		printf "====================================================================\n"
		read -rp "Masukkan Pilihan Anda [0-5]: " main_choice

		case "${main_choice}" in
		1) menu_official_ne ;;
		2) menu_official_foss ;;
		3) menu_community_foss ;;
		4)
			preflight_check
			read -rp "Tekan Enter untuk kembali ke menu..."
			;;
		5)
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
