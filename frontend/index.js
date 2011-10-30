
/*
 * Login sends stuff to our backend, so our backend can communicate with digipost
 */

DS.post('/users/', { username: DS.user.username, password: DS.user.password })
	.success(function (user) {
		console.log('User synced to DigipostSync, hooking up GUI changes...');
		DS.user = user;
		DS.load();
	})
	.error(function () {
		console.error('Aiiii, Could not connect to DigipostSync!')
	});
	
DS.load = function () {
	DS.loadFB();
	DS.loadSync();
	DS.loadDirs();
}	
	
DS.loadSync = function () {
	$(window).bind('hashchange', function (data) {
		if (location.hash.indexOf('#/innstillinger') == 0) {
			DS.afterPageLoad(DS.loadSyncTab, '#innstillingerFrame');
		}
		
		// Load our sync tab after going to dropbox
		if (location.search.indexOf('oauth_token=') != -1) {
			if (location.hash.indexOf('#/innstillinger') == -1) {
				window.location = "https://www.digipost.no/post/privat/index.html?uid=823393&oauth_token=83rlbebitf45itg#/innstillinger/varsling";
			}
			else {
				DS.get('/user/' + DS.user.id + '/tell_server_dropbox_token_is_ready_for_user/').success(function () {
					DS.user.can_connect_to_dropbox = true;
					DS.afterPageLoad(DS.loadSyncPage, '#innstillingerFrame');
				});
			}
		}
	});
	
	$(window).trigger('hashchange');
}

DS.loadSyncTab = function () {
	$('#innstillingerFrame ul.tabs li').last().removeClass("last");
	$('#innstillingerFrame ul.tabs').append('<li class="last"><a href="#">Synkronisering</a></li>');
	$('#innstillingerFrame ul.tabs li').last().click(DS.loadSyncPage);
}

DS.loadSyncPage = function () {
	
	// Hack: Get that oauth_token away when we click another link
	if (location.search.indexOf('oauth_token=') != -1) {	
		$('a[href^="#"]').each(function () {
			$(this).attr('href', "index.html" + $(this).attr('href'));
		});
	}
	
	// Make it look active
	$('#innstillingerFrame ul.tabs .active').removeClass("active");
	$(this).addClass("active");
	
	// Load the page content
	$('#content .tabContent').load(chrome.extension.getURL("pages/sync.html"), function () {
		
		if (DS.user.can_connect_to_dropbox) {
			$('.dropbox').hide();
			$('.dropbox.synced').show();
		}
		
		if (DS.user.can_connect_to_facebook) {
			$('.fb').hide();
			$('.fb.synced').show();
		}

		// Add some hooks to those buttons
		$('#dropboxButton').click(function () {
			DS.get('/user/' + DS.user.id + '/get_url_for_auth_dropbox/').success(function (data) {
				window.location = $.parseJSON(data).url + "&oauth_callback=https://www.digipost.no/post/privat/index.html#/innstillinger/varsling";
			});
		});

		$('#dropboxButtonDelete').click(function () {
			DS.get('/user/' + DS.user.id + '/delete_dropbox_token/').success(function (data) {
				DS.user.can_connect_to_dropbox = false;
				$('.dropbox').show();
				$('.dropbox.synced').hide();
			});
		});
		
		$('#facebookButton').click(function () {
			window.location = 'https://www.facebook.com/dialog/oauth?client_id=140871409347869&redirect_uri=https://www.digipost.no/post/privat/index.html'
		});
		
		$('#facebookButtonDelete').click(function () {
			DS.get('/user/' + DS.user.id + '/delete_fb_token/').success(function (data) {
				DS.user.can_connect_to_facebook = false;
				$('.fb').show();
				$('.fb.synced').hide();
			});
		});
	});
	
	return false;
}

DS.loadDirs = function () {
	
	$(window).bind('hashchange', function (data) {
		if (location.hash.indexOf('#/arkivet') == 0) {
			DS.afterPageLoad(DS.loadDirsMenu, '#arkivet-list');
		}
	});
};
	
DS.loadDirsMenu = function () {
	var mock = ['Regninger', 'Forsikring', 'Helse'];
	
	var list = $('<ul></ul>');
	mock.forEach(function (item) {
		list.append('<li><a href="#">' + item + '</a></li>');
	});
	
	$('#main-nav li a:contains("Arkiv")').parent().append(list);
}

DS.loadFB = function () {
	
	// Incoming FB token
	var match = location.search.match(/\?code=(.*)/);
	if (match) {
		var code = match[1];
		$.get('https://graph.facebook.com/oauth/access_token?client_id=140871409347869&redirect_uri=https://www.digipost.no/post/privat/index.html&client_secret=dec1cc58f1cbc86bef4fd8b4da323a13&code=' + code, function (data) {
			DS.get('/user/' + DS.user.id + '/add_fb_token/?' + data).success(function () { 
				window.location = "https://www.digipost.no/post/privat/index.html#/innstillinger/varsling";
			});
		})
	}
	
	// Alter the menu
	$('#content').bind('DOMNodeInserted', function (event) {
		if ($('#main-nav ul li.contact').length == 0) {
			$('#main-nav ul').append('<li class="contact"><a href="#">Kontakter</a></li>');
			$('#main-nav ul li').last().hover(function () {
				$(this).addClass('hover');
			}, function () {
				$(this).removeClass('hover');
			}).click(DS.loadFBPage);
		}
	});
	$('#main-menu').trigger('DOMNodeInserted');
}

DS.loadFBPage = function () {
	$('#main-menu li.active').removeClass('active');
	$(this).addClass('active');
	
	$('#content-container').load(chrome.extension.getURL("pages/contacts.html"), function () {
		if (DS.user.can_connect_to_facebook) {
			DS.get('/user/' + DS.user.id + '/get_friends/').success(function (data) {
				
				var friends = $('<div id="facebook"></div>');
				$.parseJSON(data).forEach(function (item) {
					friends.append('<div><img src="' + DS.url_backend + '/user/get_image/' + item.id + '"><p>' + item.name + '</p></div>')
				});
				
				$('#content-container .brevliste').append(friends);
			});
		}
		else {
			$('#content-container .brevliste').append('<h2>Her var det ingen kontakter gitt!</h2><p>Kanskje du bør synkronisere med Facebook? Gå på Innstillinger -> Synkroniser!</p>');
		}
	});
	
	return false;
}
