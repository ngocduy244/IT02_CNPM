window.addEventListener("load", function(){
    let addBtn = document.querySelectorAll('.add_btn')
    const patientName = document.querySelector('.name_user')
//    const patientSymptom = document.querySelector('.symptom_user')
    const inputDisease = document.querySelector('.input_disease')
    const inputSymptom = document.querySelector('.input_symptom')
    const btnConfirm = document.querySelector('.btn-confirm')
    const disease = document.querySelector('.emxamine_disease-input')
    const symptom = document.querySelector('.emxamine_symptom-input')
    const userID = document.querySelector('.user_id')
    const inputUserID = document.querySelector('.input_user_id')
    const inputUserName = document.querySelector('.input_user_name')

    btnConfirm.addEventListener("click", function(){
        inputDisease.value = disease.value
        inputSymptom.value = symptom.value
    })


    addBtn.forEach(item => item.addEventListener('click', function(){
        const patient = item.parentNode.parentNode
        const name = patient.querySelector('.patient_name')
//        const symptom = patient.querySelector('.patient_symptom')
        const id = patient.querySelector('.patient_id')

        inputUserID.value = id.textContent
        userID.textContent = id.textContent
//        inputSymptom.value = symptom.textContent
        patientName.textContent = name.textContent
        inputUserName.value = name.textContent
//        patientSymptom.textContent = symptom.textContent
        tr = item.parentNode.parentNode
        tr.parentNode.removeChild(tr)
    }))
})