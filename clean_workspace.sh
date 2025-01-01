#!/usr/bin/env bash

function main(){

    clear

    readarray -t EGG_INFO < <(find . -path "./*env" -prune -type d -o -name "*.egg-info" -print)
    readarray -t BUILD < <(find . -path "./*env" -prune -type d -o -name "build" -print)
    readarray -t PYCACHE_DIRS < <(find . -path "./*env" -prune -type d -o -name "__pycache__" -print)
    readarray -t PYTEST_DATA < <(find . -path "./*env" -prune -type d -o -name ".pytest_cache" -print)
    readarray -t COV_FILES < <(find . -path "./*env" -prune -type f -o -name ".coverage" -print)
    readarray -t LOG_FILES < <(find . -path "./*env" -prune -type f -o -name "*.log" -print)

    DATA_TO_DELETE=(${EGG_INFO[@]} ${BUILD[@]} ${PYCACHE_DIRS[@]} ${PYTEST_DATA[@]} ${COV_FILES[@]} ${LOG_FILES[@]})

    count_items=${#DATA_TO_DELETE[@]}

    echo "----------------------------------------------"

    if [ "${count_items}" -gt "0" ]; then

        printf "[+] Items to delete: %d\n\n" "${count_items}"

        for item in "${DATA_TO_DELETE[@]}"; do
            echo "[!] Deleting [${item}]"
            rm -rf "${item}"
        done
    else
        echo "[+] No data to delete found!"
    fi
    
    echo "----------------------------------------------"
}

# Entry point
current_bash_version="${BASH_VERSION%%.*}"

if [[ $current_bash_version -lt 4 ]];then
    echo "-----------------------------------------------------------------------"
    echo ""
    echo "[!] Bash version 4 or higher is required to run this script. Exiting..."
    echo ""
    echo "-----------------------------------------------------------------------"
    exit 1
fi

main