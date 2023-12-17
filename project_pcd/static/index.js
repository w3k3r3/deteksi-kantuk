// Inisialisasi variabel teks bahasa Inggris dan Indonesia
let englishtext = "";
let indotext = "";

// Event handler ketika halaman selesai dimuat
window.onload = () => {
	// Menggunakan jQuery untuk menangani klik pada tombol sendbutton
	$('#sendbutton').click(() => {
		// Mengatur ulang teks bahasa Inggris dan Indonesia
		englishtext = "";
		indotext = "";
		// Menyembunyikan antarmuka
		hideInterface();
		// Mendapatkan elemen gambar dan input dari halaman
		imagebox = $('#imagebox')
		input = $('#imageinput')[0]
		// Memeriksa apakah file gambar telah dipilih
		if(input.files && input.files[0])
		{
			let formData = new FormData();
			formData.append('image' , input.files[0]);
			formData.append("video", input.files[0]);
			// Menggunakan AJAX untuk mengirim file ke server
			$.ajax({
				url: "http://192.168.238.1:8080/project_pcd", 
				// fix below to your liking
				// url: "http://xxx.xxx.xxx.xxx:8080/detectObject", 
				type:"POST",
				data: formData,
				cache: false,
				processData:false,
				contentType:false,
				error: function(data){
					console.log("upload error" , data);
					console.log(data.getAllResponseHeaders());
					// Memperbarui antarmuka setelah terjadi kesalahan
					updateInterface();
				},
				success: function(data){
					console.log(data);
					bytestring = data['status'];
					image = bytestring.split('\'')[1];
					englishtext = data['englishmessage'];
					indotext = data['indomessage'];
					imagebox.attr('src' , 'data:image/jpeg;base64,'+image);
					// Memperbarui antarmuka setelah mendapatkan respons dari server
					updateInterface();					
				}
			});
			
		}
	});

	// Menggunakan speechSynthesis WebAPI
	const voiceEnglishOutputButton = document.getElementById('voice-english-output');
	const voiceindoOutputButton = document.getElementById('voice-indo-output');
	voiceEnglishOutputButton.addEventListener('click', () => {
		let utterance = new SpeechSynthesisUtterance(englishtext);
		utterance.lang = "en-GB";
		utterance.voice = speechSynthesis.getVoices()[5];// Google English Female
		speechSynthesis.speak(utterance);
	});
	voiceindoOutputButton.addEventListener('click', () => {
		let utterance = new SpeechSynthesisUtterance(indotext);
		utterance.lang = "id-ID";
		utterance.voice = speechSynthesis.getVoices()[10];// Google indo Female
		speechSynthesis.speak(utterance);
	});
	// Event handler ketika tombol opencam diklik
	$("#opencam").click(() => {
		console.log("evoked openCam");
		$.ajax({
			url: "/opencam",
			type: "GET",
			error: function (data) {
				console.log("upload error", data);
			},
			success: function (data) {
				console.log(data);
			}
		});
	})
};
// Fungsi untuk membaca URL gambar
function readUrl(input){
	imagebox = $('#imagebox');
	console.log("evoked readUrl");
	if(input.files && input.files[0]){
		let reader = new FileReader();
		reader.onload = function(e){
			
			imagebox.attr('src',e.target.result); 
			resizeImage();
		}
		reader.readAsDataURL(input.files[0]);
	}
}
// Fungsi untuk menyesuaikan ukuran gambar
function myResizeFunction2(y){
	if (y.matches) {
		imagebox.width(640);
		imagebox.height(640);
	}
	else {
		imagebox.width(940);
		imagebox.height(740);
	}
}
function myResizeFunction1(x) {
	imagebox = $('#imagebox');
	
	if(x.matches){
		imagebox.width(360);
		imagebox.height(360);
	}
	else{ 
		let y = window.matchMedia("(max-width:1050px)");
		myResizeFunction2(y);
		y.addListener(myResizeFunction2); // Menambahkan event listener pada setiap perubahan
	}
}
function resizeImage(){
	
	let x = window.matchMedia("(max-width:700px)");
	myResizeFunction1(x);
	x.addListener(myResizeFunction1);
	
}
// Fungsi untuk menyembunyikan antarmuka
function hideInterface(){
	$(".loading").hide();
	let progresstext = document.querySelector('.text');
	progresstext.style.display = "none"; // Menyembunyikan teks yang sudah selesai
	hideButtons();
	// Fungsi untuk menyembunyikan tombol-tombol
	function hideButtons(){
		$("#voice-english-output").hide();
		$("#voice-indo-output").hide();
	}
}
// Fungsi untuk memperbarui antarmuka
function updateInterface(){
	$(".loading").show();
	progress();

	// Menampilkan voice output setelah sekitar 18 detik
	setTimeout(
		function () {
			showTarget();
		}, 10000
	);

	function showTarget() {
		$("#voice-english-output").show();
		$("#voice-indo-output").show();
	}
}
// Fungsi untuk menampilkan progres loading
function progress() {
	let percent = document.querySelector('.percent');
	let progress = document.querySelector('.progress');
	let text = document.querySelector('.text');
	let count = 12;//4
	let per = 8;//16
	let loading = setInterval(animateProgress, 100);

	function animateProgress() {
		if (count == 100 && per == 360) {
			percent.classList.add("text-blink")
			percent.innerText = "Audio, klik jika ingin mendengarkan output"
			percent.style.fontSize = "20px";

			text.style.display = "block";
			clearInterval(loading);
		}
		else {
			per = per + 4;
			count = count + 1;
			progress.style.width = per + 'px';
			// percent.textContent = count + '%';
			percent.innerText = count + '%';
		}
	}
}
// Fungsi untuk mengubah warna tombol
function changeColor(){
	let sendButton = document.querySelector("#sendbutton");
	// let sendButton = document.getElementById("sendbutton");
	sendButton.style.backgroundColor = '#00FF33';
	sendButton.style.color = "black";
}
// Fungsi untuk menangani event ketika opencam dijalankan
function openCam(e){
	console.log("evoked openCam");
	e.preventDefault();
	console.log("evoked openCam");
	console.log(e);
}