let textarea_ru,textarea_uz,bold_open="<b>",bold_close="</b>",italic_open="<i>",italic_close="</i>";function formatButtonClick(t){let e,n,l,o,u,d=t.currentTarget.id;-1!==d.indexOf("Ru")?l=document.getElementById("text_ru"):-1!==d.indexOf("Uz")&&(l=document.getElementById("text_uz")),-1!==d.indexOf("italic")?(o=italic_open,u=italic_close):-1!==d.indexOf("bold")&&(o=bold_open,u=bold_close),n=l.selectionStart,e=l.selectionEnd;let i=l.value;if(n===e){let t=i.substring(0,n),e=i.substring(n);i=t+o+u+e,l.value=i}else{let t=i.substring(0,n),d=i.substring(n),c=(i=t+o+d).substring(0,e+3),a=i.substring(e+3);i=c+u+a,l.value=i}}document.addEventListener("DOMContentLoaded",()=>{let t=document.getElementById("boldButtonRu"),e=document.getElementById("italicButtonRu"),n=document.getElementById("boldButtonUz"),l=document.getElementById("italicButtonUz");textarea_ru=document.getElementById("text_ru"),textarea_uz=document.getElementById("text_uz"),[t,e,n,l].forEach(t=>{t.addEventListener("click",formatButtonClick)})});