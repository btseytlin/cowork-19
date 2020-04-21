function confirm_delete(post_id){
    const r = confirm("Точно удалить?");
    if (r === true) {
      window.location.href = "/archive/"+post_id
    }
}


function createCookie(name,value,days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}

function eraseCookie(name) {
	createCookie(name,"",-1);
}


function isWelcomeHidden(){
    if (readCookie('welcome-hidden') != null) {
        return true;
    }
    return false;
}

function showWelcome(){
    const welcome_elem = document.getElementById('welcome');
    if (welcome_elem) {
        welcome_elem.classList.remove("hidden");
    }
}

function hideWelcome(){
    const welcome_elem = document.getElementById('welcome');
    if (welcome_elem) {
        welcome_elem.classList.add("hidden");
    }
}


function closeWelcome(){
    createCookie('welcome-hidden', '1', 999)
    hideWelcome();
}



window.onload = function(){
    const welcome_hidden = isWelcomeHidden();
    if (welcome_hidden === false) {
        showWelcome()
    }
}