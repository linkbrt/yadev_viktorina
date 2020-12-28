const form = document.querySelector('.quiz__right')
const checkboxes = document.querySelectorAll('.mdl-checkbox__input');
const button = document.querySelector('.quiz__button');
const inputField = document.querySelector('.mdl-textfield__input')


//form.addEventListener('change', function(){
//  let disabled = true;
//  checkboxes.forEach(function(item, i, arr) {
//    if (item.checked) disabled = false;
//  });
//  button.disabled = disabled;
//})

checkboxes.forEach(function(item, i, arr) {
  item.addEventListener('change', function(){
    let disabled = true;
    if (item.checked) disabled = false;
    button.disabled = disabled;
  })
});




inputField.addEventListener('input', function(){
  let disabled = true;
  if (inputField.value.length > 0) disabled = false;
  button.disabled = disabled;
})
