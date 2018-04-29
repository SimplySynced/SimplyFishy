$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port)
    socket.on('connect', function() {
        socket.emit('my_message', 'User connected!');
    });

    socket.on('float_sw', function(msg) {
         $('#floatsw_msg').html('<p>' + msg.data + '</p>');
         console.log(msg.data)
     });

    //Setup interval to check temp every 5 seconds
    //setInterval(function(){
    //    socket.emit('read_temp');
    //}, 5000);

    socket.on('tempprobe_1', function(temp) {
        $('#tempprobe_1_temp').html('<p>' + temp.data + '</p>');
        console.log(temp.data)
    });

});

function addNoteData() {

    $("#addNote").on('submit', function (e) {
        e.preventDefault();

        var notedata = $(this).serialize();
        //console.log(notedata);

        $.post("actions.php?fn=addNote",notedata)
            .done(function( data ) {
                $('#addNoteSuccess').text(data);
                $('#addNoteSuccess').css("color", "green");
                $('#addNoteSuccess').css("float", "right");
                $('#notes').val('');
            });
    });

}

function deleteNote( id ) {

    console.log(id);

    var answer = confirm('Are you sure you want to delete this note?');

    if ( answer ) {
        $.post("actions.php?fn=deleteNote&id="+id)
    }
}

function addTest() {

    $(".aT").on('click', function(e) {
        e.preventDefault();

        var testData = $('#testData').serialize();

        $.post("actions.php?action=add_test", testData)
            .done(function () {
                $("#testModal").modal('hide');
                location.reload(true);
            });
    });
}
;