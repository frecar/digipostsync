
/*
 * Quick and dirty logging of user credentials
 * Sent to the backend once we get in. This is of course a huge securyity faux pau, and there are several use cases where this 
 * will fail really badly (several tabs, etc) but it works for our hacky purposes :)
 */

$('#username').keyup(function () {
	localStorage.setItem('ds_username', $(this).val());
}).attr('autocomplete', 'on');

$('#password').keyup(function () {
	localStorage.setItem('ds_password', $(this).val());
}).attr('autocomplete', 'on');