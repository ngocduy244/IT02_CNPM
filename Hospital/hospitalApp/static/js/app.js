// dropdown user role
const dropdownItem = document.querySelectorAll(".dropdown-list_item")
const dropdownSelect = document.querySelector(".dropdown-select")
const dropdownSelected = document.querySelector(".dropdown-selected")
const dropdownList = document.querySelector(".dropdown-list")
const dropdown = document.querySelector(".dropdown")
const inputRole = document.querySelector('.selected-role')

const icon = document.querySelector(".icon")


function handleDropdown(){
    dropdownList.classList.toggle("show")
    icon.classList.toggle("fa-caret-up")
    icon.classList.toggle("fa-caret-down")
}

dropdownSelect.addEventListener("click", handleDropdown)

dropdownItem.forEach(item => item.addEventListener("click", function(e){
    dropdownSelected.textContent = item.textContent
    inputRole.value = item.textContent
    icon.classList.remove("fa-caret-up")
    icon.classList.add("fa-caret-down")
    dropdownList.classList.remove("show")
}))

document.addEventListener("click", function(e){
    if(!dropdown.contains(e.target)){
        dropdownList.classList.remove("show")
        icon.classList.remove("fa-caret-up")
        icon.classList.add("fa-caret-down")
    }
})

