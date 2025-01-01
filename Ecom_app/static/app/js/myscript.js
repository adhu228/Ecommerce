$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})

$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})



// $(document).on('click', '.remove-cart', function (e) {
//     e.preventDefault();
//     var prod_id = $(this).attr('pid');
//     $.ajax({
//         url: "{% url 'remove_cart' %}",
//         method: 'GET',
//         data: { 'prod_id': prod_id },
//         success: function (response) {
//             if (response.cart_empty) {
//                 // Update UI to show "Cart is Empty" if the cart is empty
//                 $('.container.my-5 .row').html('<h1 class="text-center mb-5">Cart is Empty</h1>');
//             } else {
//                 // Update totals
//                 $('#amount').text('Rs.' + response.amount.toFixed(2));
//                 $('#totalamount').text('Rs.' + response.totalamount.toFixed(2));
//                 // Remove the specific cart item
//                 $('#cart-item-' + prod_id).remove();
//             }
//         },
//         error: function (xhr, status, error) {
//             alert('Error: Unable to remove item. Please try again.');
//         }
//     });
// });









$('.plus-wishlist').click(function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/pluswishlist",
        data: {
            prod_id: id
        },
        success: function(data){
            // Correct string interpolation using backticks
            window.location.href = `http://localhost:8002/product-detail/${id}`;
        }
    });
});

$('.minus-wishlist').click(function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: {
            prod_id: id
        },
        success: function(data){
            // Correct string interpolation using backticks
            window.location.href = `http://localhost:8002/product-detail/${id}`;
        }
    });
});
