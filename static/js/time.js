let date = document.querySelector('.date');
let hour = document.querySelector('.hour');
let minute = document.querySelector('.minute');
let second = document.querySelector('.second');

function refreshTime(){
  window.requestAnimationFrame(refreshTime);
  let d = new Date();
  let year = d.getFullYear();
  let month = d.getMonth();
  let data = d.getDate();
  let hr = d.getHours();
  let mins = d.getMinutes();
  let sec = d.getSeconds();
  var arrWeek = new Array("日", "一", "二", "三", "四", "五", "六");
  let i = new Date().getDay();
  let week = "(" + arrWeek[i] + ")";
  date.innerText = year + "-" + zeroStuffing((month + 1)) + "-" + zeroStuffing(data) + " " + week
  hour.innerText = zeroStuffing(hr);
  minute.innerText = zeroStuffing(mins);
  second.innerText = zeroStuffing(sec);
}

function zeroStuffing(str){
  return str < 10 ? `0${str}` : str;
}

refreshTime();
