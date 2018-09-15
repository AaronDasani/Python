
$(document).ready(function(){

    $(".addcart").click(function () {
        console.log($(this).css("background-color"))
        if($(this).css('border-color')=='rgb(108, 117, 125)'){
            $(this).css('background-color', 'gold');
            $(this).css('border-color', 'gold');
        }else {
            $(this).css('background-color', 'transparent');
            $(this).css('border-color','rgb(108, 117, 125');
            $(this).css("color",'rgb(108, 117, 125');
        }
        
        return false;
        
    })
   






    


});