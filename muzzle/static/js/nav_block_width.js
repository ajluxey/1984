// for correction navigation block width

function corrector() {
    let menu = document.getElementById('menu');
    let menuBlocks = menu.getElementsByClassName('menu');
    blocksCount = menuBlocks.length
    for (let i = 0; i < blocksCount; i++) {
        menuBlocks[i].style.width = 100/blocksCount + '%';
    }

    if (document.getElementsByClassName('modal_message').length > 0){
        modal();
    }
}

corrector();

// modal window

function modal() {
    let modal_el = document.getElementById('modal');
    modal_el.style.display = 'block';
    let modal_content = document.getElementById('modal_win');
    for (let arg of arguments){
        switch (arg){
            case 'progress':
                progress_bar = document.createElement('progress');
                up_mess = document.createElement('h3');
                percents = document.createElement('h4');

                up_mess.innerHTML = 'Загрузка';
                modal_content.append(up_mess);

                progress_bar.setAttribute('id', 'progress_bar');
                modal_content.append(progress_bar);

                percents.innerHTML = '50%';
                percents.setAttribute('id', 'percents')
                modal_content.append(percents);

                progress_bar.max = 100;
                progress_bar.value = 0;
                while (progress_bar.value < 50) {
                    sleep(10);
                    progress_bar.value += 1;
                }
                break
        }
    }
}


function modalCloser(){
    let modal_el = document.getElementById('modal');
    if (modal_el.hasAttribute('style')){
        let modal_content = document.getElementById('modal_win');
        let closer = document.getElementById('modal_closer');
        modal_content.innerHTML = '';
        modal_content.append(closer);
        modal_el.removeAttribute('style');
    }
}


function sleep(ms) {
    ms += new Date().getTime();
    while(new Date() < ms){}
}

//window.onclick = function(event){
//    let modal_el = document.getElementById('modal');
//    let modal_win = document.getElementById('modal_win');
//    if (event.target != modal_el){
//        modalCloser();
//    }
//};
