function clear_highlighting() {
  const elements_with_hightlighter = Array.from(document.getElementsByClassName("HIGHLIGHTING"));
  elements_with_hightlighter.forEach(function (element) {
    element.style.backgroundColor = null;
  });
}
async function amend_page(instruction_name, bit_no, instruction_fields, field_name) {
}
async function highlight_bit(instruction_name, bit_no, instruction_fields, field_name) {
  clear_highlighting();
  field_value = instruction_fields[field_name]
  await amend_page(instruction_name, bit_no, instruction_fields, field_name)
  const elements_i = Array.from(document.getElementsByClassName("HIGHLIGHTING_instruction_" + instruction_name));
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
  for (const field in instruction_fields) {
    const elements_f = Array.from(document.getElementsByClassName("FIELD_" + field + "_dec"));
    elements_f.forEach(function (element) {
      element.innerHTML = parseInt(instruction_fields[field], 2)
    });
    const elements_m = Array.from(document.getElementsByClassName("MARKING_field_value_" + field + "_" + instruction_fields[field]));
    elements_m.forEach(function (element) {
      element.style.color = "blue";
    });
    
  }
}