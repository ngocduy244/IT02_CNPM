function addToCart(id, name, kind, unit, price){
    fetch('/api/cart',{
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "kind": kind,
            "unit": unit,
            "price": price
       }),
       headers: {
            "Content-Type": "application/json"
       }
    }).then(function(res){
        return res.json()
    }).then(function(data){
        console.log(data)
        let d = document.querySelector('.cart-counter')
        d.textContent = data.total_quantity
    })
}


function updateCart(medicineId, obj){
    fetch(`/api/cart/${medicineId}`,{
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
       }),
       headers: {
            "Content-Type": "application/json"
       }
    }).then(function(res){
        return res.json()
    }).then(function(data){
        let d = document.querySelectorAll('.cart-counter')
        for(let i = 0; i < d.length; i++)
            d[i].textContent = data.total_quantity

        let c = document.querySelectorAll('.cart-amount')
        for(let i = 0; i < c.length; i++)
            c[i].textContent = data.total_amount.toLocaleString("en-US")
    })
}


function deleteCart(medicineId){
    if(confirm("Bạn có chắc chắn xóa chứ?")==true){
         fetch(`/api/cart/${medicineId}`,{
            method: "delete",
            }).then(function(res){
                return res.json()
            }).then(function(data){
                let d = document.querySelectorAll('.cart-counter')
                for(let i = 0; i < d.length; i++)
                    d[i].textContent = data.total_quantity

                let c = document.querySelectorAll('.cart-amount')
                for(let i = 0; i < c.length; i++)
                    c[i].textContent = data.total_amount.toLocaleString("en-US")
            })

          let el = document.getElementById(`cart${medicineId}`)
          el.style.display = "none"
    }
}


function pay(){
    if(confirm("Bạn chắc chắn lưu chứ?")){
        disease =  document.getElementById("diseaseName").value
        symptom =  document.getElementById("symptomName").value
        userID =  document.getElementById("userIdName").value

        fetch('/api/prescription', {
        method: "post",
        body: JSON.stringify({
            "disease": disease,
            "symptom": symptom,
            "userID": userID,
           }),
           headers: {
                "Content-Type": "application/json"
           }
        }).then(function(res){
            return res.json()
        }).then(function(data){
           if(data.status===200){
               alert("Toa thuốc được thêm thành công")
               location.reload()
           }

           else if (data.status===204){
                alert("Bệnh nhân đã được khám ngày hôm nay")
           }
        })
        }
}

const dropdownMedicine = document.querySelectorAll(".dropdown-list_medicine")
const btn = document.querySelector('.btn-js')

dropdownMedicine.forEach(item => item.addEventListener("click", function(e){
    btn.setAttribute("data-id", item.dataset.id)
    btn.setAttribute("data-name", item.dataset.name)
    btn.setAttribute("data-kind", item.dataset.kind)
    btn.setAttribute("data-unit", item.dataset.unit)
    btn.setAttribute("data-price", item.dataset.price)
}))

btn.addEventListener("click", function(e){
    let id = parseInt(e.target.dataset.id)
    let name = e.target.dataset.name
    let kind = e.target.dataset.kind
    let unit = e.target.dataset.unit
    let price = parseInt(e.target.dataset.price)
//    console.log(typeof id)
    if(!id || !name || !kind || !unit || !price)
       alert("Bạn phải chọn loại thuốc")
    else
        addToCart(id,name,kind,unit,price)

    location.reload();
})