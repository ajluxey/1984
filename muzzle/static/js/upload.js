function nameFromPath(path) {
    let name = path.replace(/^.*[\\\/]/, '');
    return name;
}

document.getElementById("image").onchange = function() {
    name = nameFromPath(this.value);
    if (name.trim() == ''){
        name = 'Выберите образ';
    }
    document.getElementById("image_name").innerHTML = name;

    if (name != 'Выберите образ'){
        let data = new FormData();
        data.append('name', name);
        fetch('/images/check_file_exists', {method: 'POST', body: data})
            .then(response => response.json())
            .then(result => {
                if (result.exists)
                    if (!confirm('Такой файл уже существует, перезаписать?')) {
                        document.getElementById("image").value = '';
                        document.getElementById("image_name").innerHTML = 'Выберите образ';
                    }
            });
    }
};

document.getElementById("config").onchange = function() {
    name = nameFromPath(this.value);
    defCheckbox = document.getElementById("default_config");

    if (name.trim() == ''){
        name = 'Выберите кофигурацию';
        defCheckbox.checked = true;
    } else {
        defCheckbox.checked = false;
    }
    document.getElementById("config_name").innerHTML = name;
};

// form for uploading
document.getElementById("trigger").onclick = function() {
    form = document.getElementById("close_up_form");
    if (form.classList.contains("close") && !form.classList.contains("open")){
        form.classList.remove("close");
        form.classList.add("open");
    } else if (!form.classList.contains("close") && form.classList.contains("open")){
        form.classList.remove("open");
        form.classList.add("close");
    }
}

function showDelete(element){
    deleteBut = element.querySelectorAll('div')[2];
    if (deleteBut.classList.contains('close')){
        deleteBut.classList.remove('close');
    }
}