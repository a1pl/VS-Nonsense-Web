(function() {
if(window.location.protocol !== 'file:') return;

const insertCredit = () => {
	const credit = '<div id="playmore" style="position: fixed; bottom: 10px; left: 50%; transform: translateX(-50%); z-index: 9999; padding: 10px 15px; background: rgba(0,0,0,0.8); border: 2px solid #fff; border-radius: 5px;"><a href="gn-math.dev" target="_blank" style="color: #fff; text-decoration: none; font-family: Arial, sans-serif; font-size: 12px;">skidded by willowy</a></div>';
	window.document.body.insertAdjacentHTML('beforeend', credit);
};

const adjustContent = () => {
	const content = document.getElementById("openfl-content");
	if(content) content.style.height = "calc(100% - 28px)";
};

const handleCountdown = () => {
	if(window.location === window.parent.location || typeof countDownDate === 'undefined') return;
	
	const now = new Date().getTime();
	const distance = countDownDate - now;
	
	if(distance <= 0) return;
	
	setInterval(() => {
		const current = new Date().getTime();
		const remaining = countDownDate - current;
		
		if(remaining <= 0) {
			document.body.style.backgroundColor = "white";
			document.body.innerHTML = "";
		}
	}, 1000);
};

insertCredit();
adjustContent();
handleCountdown();

console.log = function() {};

})();

window.addEventListener('load', () => {
	window.focus();
	document.body.addEventListener('click', () => window.focus(), false);
});

window.addEventListener('keydown', (e) => {
	if([32, 37, 38, 39, 40].includes(e.keyCode)) {
		e.preventDefault();
	}
}, false);