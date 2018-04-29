function socket_onoff ( socket ) {

	var onOff = $('#button_'+socket).data('state');
	console.log(onOff);

	if (onOff=='0') {
		$.post("api.php?fn=on&socket="+socket);
		$('#button_'+socket).data('state', '1');
	}
	else if (onOff=='1') {
		$.post("api.php?fn=off&socket="+socket);
		$('#button_'+socket).data('state', '0');
	}

}