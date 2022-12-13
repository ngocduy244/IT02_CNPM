
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

        })
}}

function checkUser(){
        userID = document.querySelector(".user-id").value
        fetch('/api/user', {
        method: "post",
        body: JSON.stringify({
            "userID": userID,
           }),
           headers: {
            "Content-Type": "application/json"
           }
        }).then(function(res){
            return res.json()
        }).then(function(data){
            if(data.status === 200){
                let u = data.user
                let d = document.querySelector('.table')
                d.innerHTML = `
                     <tr class="">
                          <th cope="col">Mã bệnh nhân</th>
                          <th cope="col">Tên bệnh nhân</th>
                          <th cope="col">Giới tính</th>
                      </tr>
                `

                h = `
                    <tr>
                        <td> ${u.id} </td>
                        <td> ${u.name} </td>
                        <td> ${u.gender} </td>
                    </tr>
                `

                d.insertAdjacentHTML("beforeEnd", h)
            }

            else if(data.status===500){
                alert("Không có bệnh nhân mà bạn tìm")
                location.reload()
            }
        })
}
