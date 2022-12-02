window.addEventListener("load", function(){
 // fixed menu
    function debounceFn(func, wait, immediate) {
        let timeout;
        return function () {
          let context = this,
            args = arguments;
          let later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
          };
          let callNow = immediate && !timeout;
          clearTimeout(timeout);
          timeout = setTimeout(later, wait);
          if (callNow) func.apply(context, args);
        };
     }

    const header = document.querySelector(".header")
    const headerHeight = header && header.offsetHeight
    // if(header)
    //  headerHeight = header.offsetHeight

    window.addEventListener("scroll",debounceFn(function(e){
        const scrollY = window.pageYOffset
        console.log(scrollY)
        if(scrollY >= headerHeight){
            header.classList.add("is-fixed")
        }
        else{
            header.classList.remove("is-fixed")
        }
    }, 100))

//    menu link
    const links = [...document.querySelectorAll(".menu-link")]
    links.forEach(item => item.addEventListener("mouseenter", handleHoverLink))

    const line = document.createElement("div")
    line.className = "line-effect"
    this.document.body.appendChild(line)
    function handleHoverLink(e){
        console.log(e.target.getBoundingClientRect())
        const {left, top, width, height} = e.target.getBoundingClientRect()
        const offsetBottom = 5
        line.style.display = "block"
        line.style.left = `${left}px`
        line.style.width = `${width}px`
        line.style.top = `${top + height + offsetBottom}px`
    }
    const menu = document.querySelector(".menu")
    menu.addEventListener("mouseleave", function(){
        line.style.width = 0;
    })
})