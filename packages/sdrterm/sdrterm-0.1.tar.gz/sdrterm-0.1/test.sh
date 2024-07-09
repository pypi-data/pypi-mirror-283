export OUT_PATH="/tmp";
declare -A sums;
sums["${OUT_PATH}/out-155625000.wav"]="38acd5677b3e813eea185523d47b9076";
sums["${OUT_PATH}/out-155685000.wav"]="4cae5a0dfbbe4bd06ea4de41988bd606";
sums["${OUT_PATH}/out-155700000.wav"]="2eaa5e1e736f3b68e67c3b89d1407e1e";
sums["${OUT_PATH}/outB.wav"]="b8058749ff0e25eab70f92dda86c2507";
sums["${OUT_PATH}/outd.wav"]="d51e36787d2cf8a10be87a1e123bb976";
sums["${OUT_PATH}/outf.wav"]="07e31be2ff4f16b91adcf540a570c03e";
sums["${OUT_PATH}/outh.wav"]="576409e4a3cd5e76950aa0134389d75a";
sums["${OUT_PATH}/outi.wav"]="07e31be2ff4f16b91adcf540a570c03e";
sums["${OUT_PATH}/outi16.wav"]="9f21f81dd274b3695adbb0418f787b48";
sums["${OUT_PATH}/outu8.wav"]="18f1c6cbe373121a3f4c1bfe9f282467";

time ./example_simo_file.sh -i src/uint8.wav --vfos=15000,-60000 -w5k -c-3.5E+5 -t155.685M -vv -d64 \
  | grep "Total" - \
  | grep -E --color=always '[0-9]+' -;
./example.sh /mnt/d/SDRSharp_20160101_231914Z_12kHz_IQ.wav;

declare -A z="( `sed -E "s/^((\d|\w)+)\s*((\d|\w|\/|\-|\.)+)$/[\3]=\1/g" <<< $(md5sum ${OUT_PATH}/*.wav)` )";
for i in "${!sums[@]}"; do
  [[ "${sums["$i"]}" == "${z["$i"]}" ]] && echo "checksum matched: ${i}" || echo "FAILED: ${i}";
  rm "$i";
done