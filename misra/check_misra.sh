#!/bin/bash

script_folder="$(dirname $(readlink -f $0))"

echo "current working dir are $script_folder"

# Initialize variables with defaults
# the following "$script_folder/../../../frameworks/autocore" are the
# default source_folder to check, and user could still using "-s" option
# to specify the custom directory that to be checked
# for example, we could use:
# ```
# bash check_misra.sh -s "/home/work/test/vela/frameworks/test_autocore"
# ```
# to specify the project we need to check
# Please note that we need to specify the full path with "-s" option
# not relative path, such as:
# ```
# bash check_misra.sh -s "../../../frameworks/test_autocore"
# ```
# is invalid
source_folder="$script_folder/../../../frameworks/autocore" # -s, --source
out_folder="$script_folder/.results"                        # -o, --out
cppcheck_path="$script_folder/cppcheck_tool/"               # -c, --cppcheck
quiet=0                                                     # -q, --quiet
output_xml=0                                                # -x, --xml

function parse_command_line() {
   while [ $# -gt 0 ] ; do
    case "$1" in
      -s | --source) source_folder="$2" ;;
      -o | --out) out_folder="$2" ;;
      -c | --cppcheck) cppcheck_path="$2" ;;
      -q | --quiet) quiet=1 ;;
      -x | --xml) output_xml=1 ;;
      -*)
        echo "Unknown option: " $1
        exit 1
        ;;
    esac
    shift
  done
}

parse_command_line "$@"

cppcheck_bin="${cppcheck_path}/cppcheck"
cppcheck_misra="${cppcheck_path}/addons/misra.py"
cppcheck_htmlreport_tool="${script_folder}/htmlreport/cppcheck-htmlreport"

num_cores=`getconf _NPROCESSORS_ONLN`
let num_cores--

# before perform checking, we need to parse the $source_folder/Makefile
# and parse out the header file include path, such as the following:
# CFLAGS += -I$(APPDIR)/frameworks/autocore/os/include
APPDIR="$script_folder/../../.."
# the path to specify the header file path
header_include_full_path=""
if [ -f $source_folder/Makefile ]; then
  echo "start to parse the '$source_folder/Makefile' to get the header info path"
  header_include_path=$(grep -E "CFLAGS\s*\+=\s*\-I\\$\([A-Z]*\)\/" $source_folder/Makefile)

  orig_path=$(echo $header_include_path | awk -F ' ' '{print $3,$6,$9}')
  echo $orig_path

  first_stage=$(echo $orig_path | sed -e "s/ /\" /g")
  second_stage=$(echo $first_stage | sed -e "s/$/\"/g")
  third_stage=$(echo $second_stage | sed -e "s/-I/-I \"/g")
  fourth_stage=$(echo $third_stage | sed -e "s/(//g")
  final_path=$(echo $fourth_stage | sed -e "s/)//g")

  echo "the include check path are --> ${final_path}"
  header_include_full_path=$(eval echo $final_path)

else
  echo "fatal error!!! fail to get the header file include path"
  exit 1
fi

src_file_list=`find $source_folder -name "*.c"`

echo "the include check path are $header_include_full_path"

mkdir -p "$out_folder"

cppcheck_parameters=( --inline-suppr
                      --language=c
                      --enable=warning
                      --enable=information
                      --enable=performance
                      --enable=portability
                      --enable=style
                      --enable=missingInclude
                      --addon="$script_folder/misra.json"
                      --suppressions-list="$script_folder/suppressions.txt"
                      --suppress=missingIncludeSystem:*
                      --suppress=unmatchedSuppression:*
                      --suppress=cstyleCast:*
                      --platform=arm32-wchar_t2
                      --library=autocore
                      --cppcheck-build-dir="$out_folder"
                      -j "$num_cores"
                      $header_include_full_path
                      -D__cppcheck__
                      -DOSB_TOOL=OSB_gnu
                      -DOS_KERNEL_TYPE=OS_FUNCTION_CALL
                      $src_file_list
                      )

echo "source folder are $source_folder"

cppcheck_out_file="$out_folder/results.txt"
if [ $output_xml -eq 1 ]; then
  cppcheck_out_file="$out_folder/results.xml"
  cppcheck_parameters+=(--xml)
fi

"$cppcheck_bin" ${cppcheck_parameters[@]} 2> $cppcheck_out_file

# Count lines for Mandatory or Required rules
error_count=`grep -i "Mandatory - \|Required - " < "$cppcheck_out_file" | wc -l`

if [ $quiet -eq 0 ]; then
  cat "$cppcheck_out_file"
fi
echo $error_count MISRA violations
echo $error_count > "$out_folder/error_count.txt"

# we need to detect if the "-x" option is specified, then we could
# convert the final result to html format
if [ $output_xml -eq 1 ]; then
  # the cppcheck_htmlreport depends on python-pygments, we could install
  # this tools by:
  # sudo apt-get install python-pygments
  echo "start to convert the $cppcheck_out_file to readable html format"
  $cppcheck_htmlreport_tool --file=$cppcheck_out_file --report-dir=.html_result --source-dir=$source_folder
fi

exit 0
