'use strict';
function fun1() {
	var checkbox = document.querySelectorAll('button');
	var form = document.querySelectorAll('form#form');
		
	for (let index = 0; index < checkbox.length; index++) {
		if (checkbox[index].form[2].checked){
			form[index].submit();
			break;
		}
		
	}
}
