
function register_account(){

        name =  document.getElementById("name").value
        gender =  document.getElementsByName('gender');
        let len = gender.length;
        let checkValue = '';

        for (const radioButton of gender) {
                if (radioButton.checked) {
                    checkValue = radioButton.value;
                    break;
                }
            }




        birthday =  document.getElementById("birthday").value;
        address =  document.getElementById("address").value;
        phone =  document.getElementById("phone").value;
        identity_card = document.getElementById('identity_card').value


        user_name =  document.getElementById("username").value;
        password =  document.getElementById("password").value;
        confirm =  document.getElementById("confirm").value;
        avatar =  document.getElementById('avatar').files[0];


        fetch('/api/account', {
        method: "post",
        body: JSON.stringify({
            "name": name,
            "gender": checkValue,
            "birthday": birthday,
            "identity_card": identity_card,
            "address": address,
            "phone": phone,
            "user_name": user_name,
            "password": password,
            "confirm": confirm,
            "avatar": avatar,
           }),
           headers: {
                "Content-Type": "application/json"
           }
        }).then(function(res){
            return res.json()
        }).then(function(data){
           if(data.status===200){
                alert("Tạo tài khoản thành công");
                location.reload()
           }
        })

}