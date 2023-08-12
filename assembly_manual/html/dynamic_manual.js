function clear_highlighting() {
  const elements_with_hightlighter = Array.from(document.getElementsByClassName("HIGHLIGHTING"));
  elements_with_hightlighter.forEach(function (element) {
    element.style.backgroundColor = null;
  });
}
async function amend_page(field_value, bit_no, field_name) {
}
async function highlight_bit(instruction, field_value, bit_no, field_name) {
  clear_highlighting();
  await amend_page(field_value, bit_no, field_name)
  const elements_i = Array.from(document.getElementsByClassName("HIGHLIGHTING_instruction_" + instruction.toString()));
  elements_i.forEach(function (element) {
    element.style.backgroundColor = "yellow";
  });
  const elements_b = Array.from(document.getElementsByClassName("HIGHLIGHTING_bit_" + bit_no.toString()));
  elements_b.forEach(function (element) {
    element.style.backgroundColor = "orange";
  });
  const elements_f = Array.from(document.getElementsByClassName("HIGHLIGHTING_field_" + field_name));
  elements_f.forEach(function (element) {
    element.style.backgroundColor = "yellow";
  });
  const elements_v = Array.from(document.getElementsByClassName("HIGHLIGHTING_field_value_" + field_name + "_" + field_value));
  elements_v.forEach(function (element) {
    element.style.backgroundColor = "yellow";
  });
}