
function saveReceipt(){
    if(confirm("Bạn chắc chắn lưu chứ?")){
        prescriptionId =  document.getElementById("prescription_id").textContent
        totalPrice =  parseInt(document.getElementById("medicine_total_price").value)
        userID =  document.getElementById("patient_id").textContent

        fetch('/api/receipt', {
        method: "post",
        body: JSON.stringify({
            "prescriptionId": prescriptionId,
            "totalPrice": totalPrice,
            "userID": userID,
           }),
           headers: {
                "Content-Type": "application/json"
           }
        }).then(function(res){
            return res.json()
        }).then(function(data){
           if(data.status===200){
                alert("Lập hóa đơn thành công") ;
                document.querySelector('.receipt_body').innerText = ""
           }
           else if(data.status===204){
               alert('Hóa đơn này đã được lập')
               document.querySelector('.receipt_body').innerText = ""
           }

        })
        }
}