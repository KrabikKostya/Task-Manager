'use strict';
function fun1() {
    var checkbox = document.getElementById('tasckStatusPeriodical');
	var fild = document.getElementById('tasckPeriodical')
	if (checkbox.checked) {
		fild.classList.add("shown");
		fild.classList.remove("hidden");
	}else{
		fild.classList.add("hidden");
		fild.classList.remove("shown");
	}
}
