$(document).ready(function(){
    $('#messageBody').scrollTop($('#messageBody')[0].scrollHeight);

    $('#myform').submit(function(event){
        var data = $('input[name=text]').val();
        
        $( '<div class="row justify-content-start" style="margin-left:0px">' +
        '<div class="you h5">'+data+'</div>' +
        '</div>' ).appendTo( "#messageBody" );

        $('#messageBody').scrollTop($('#messageBody')[0].scrollHeight);
        
    })
})