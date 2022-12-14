
function saveMC(){
if(confirm("Bạn chắc chắn lưu chứ?")){
        userID = document.querySelector(".user-id").value
        date =  document.querySelector("#examine_date").value

        fetch('/api/medicalCertificate', {
        method: "post",
        body: JSON.stringify({
            "userID": userID,
            "date": date,
           }),
           headers: {
                "Content-Type": "application/json"
           }
        }).then(function(res){
            return res.json()
        }).then(function(data){
           if(data.status===200){
                alert("Lập phiếu khám bệnh thành công") ;
                location.reload()
           }
           else if(data.status===204){
               alert('Bệnh nhân đã đăng kí khám ngày này')
               location.reload()
           }

           else if(data.status===206){
               alert(` Số lượng bệnh nhân đã vượt ${data.amount} người`)
               location.reload()
           }

        })
}}


