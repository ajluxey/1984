from flask import Blueprint
from flask import render_template, request, flash, jsonify
from muzzle import app
from werkzeug.utils import secure_filename
import os, codecs, shutil, json, time

images = Blueprint('images', __name__, template_folder='templates', static_folder='static')


@images.route('/')
def img_index():
    return render_template('img_index.html', links=app.config['ALL_LINKS'])


@images.route('/management', methods=['post', 'get'])
def management():
    image_list = []  # {'name': 'image', 'desc': 'description'}
    image_folders = app.config['IMAGE_FOLDER']
    for image in os.listdir(image_folders):
        image_temp = {}
        if not os.path.isdir(os.path.join(image_folders, image)):
            continue
        image_temp['name'] = image
        folder = os.path.join(image_folders, image)
        for file in os.listdir(folder):
            if file.startswith('README'):
                with codecs.open(os.path.join(image_folders, folder, file), 'r', 'utf-8') as f:
                    image_temp['desc'] = f.read()
                break
        image_list.append(image_temp)

    # form = UploadForm()
    if request.method == 'POST':
        if request.form.get('delete_but'):
            if delete_from_server(request.form.get('delete_but')):
                flash("Удаление прошло успешно")
            else:
                flash("Что-то пошло не так, не удалось удалить")

        else:
            if request.form.get('default_config'):
                image = request.files['image']
                description = request.form.get('description')
                if upload_to_server(image, app.config['BASE_CONFIG'], description):
                    flash('Что-то пошло не так, не удалось загрузить')
                else:
                    flash('Успешно загружено')
            else:
                image = request.files['image']
                config = request.files['config']
                description = request.form.get('description')
                if upload_to_server(image, config, description):
                    flash('Что-то пошло не так, не удалось загрузить')
                else:
                    flash('Успешно загружено')
    return render_template('management.html', links=app.config['ALL_LINKS'], images=image_list)


@images.route('/check_file_exists', methods=['post'])
def check_file_exists():
    name = request.values.get('name')
    answer = name in os.listdir(app.config['IMAGES'])
    return jsonify(exists=answer)


@images.route('/distribute', methods=['post', 'get'])
def distribute():
    map = app.config['MAP']
    macs = app.config['MACS']
    image_list = []
    images_fold = app.config['IMAGE_FOLDER']
    for image in os.listdir(images_fold):
        if os.path.isdir(os.path.join(images_fold, image)):
            image_list.append(image)
    config = {}
    for image in image_list:
        config[image] = []
    if request.method == 'POST':
        if request.form.get('default_to_all'):
            image_for_all = request.form.get('image_for_all')
            if image_for_all != 'default':
                config['default'] = image_for_all
            else:
                config['default'] = None
        else:
            for mac in macs:
                image = request.form.get(mac)
                if image == 'default':
                    continue
                config[image].append(mac)
            config['default'] = None
        if create_master_config(config):
            flash('Мастер конфиг был создан')
    macs_with_images = get_master_config()
    image_list.insert(0, 'default')
    return render_template('distribute.html', links=app.config['ALL_LINKS'],
                           map=map,
                           images=image_list,
                           macs_with_images=macs_with_images)


def upload_to_server(*files):
    for file in files:
        if isinstance(file, str):
            continue
        if file.filename == '':
            return 1
    image = files[0]
    config = files[1]
    description = files[2]

    image_name = secure_filename(image.filename)
    clear_name = '.'.join(image_name.split('.')[:-1])

    if not os.path.exists(os.path.join(app.config['IMAGE_FOLDER'], clear_name)):
        os.mkdir(os.path.join(app.config['IMAGE_FOLDER'], clear_name))

    image_path = os.path.join(app.config['IMAGES'], image_name)
    image.save(image_path)
    # os.symlink(image_path, os.path.join(app.config['IMAGE_FOLDER'], clear_name, image.filename))
    path = os.path.join(app.config['IMAGE_FOLDER'], clear_name)

    # if config is default
    if isinstance(config, str):
        with open(os.path.join(path, 'config.sh'), 'w') as conf:
            conf.write(config.format(imagename=image.filename))
    else:
        config.save(os.path.join(path, 'config.sh'))
    with open(os.path.join(path, 'README'), 'w', encoding="utf-8") as desc:
        desc.write(description)
    return 0


def delete_from_server(name):
    path = app.config['IMAGE_FOLDER']
    if os.path.exists(os.path.join(path, name)):
        shutil.rmtree(os.path.join(path, name))
    else:
        return False

    path = app.config['IMAGES']
    for image in os.listdir(path):
        clear_name = '.'.join(image.split('.')[:-1])
        if clear_name == name:
            os.remove(os.path.join(path, image))

    config = app.config['MASTER_CONFIG']
    if os.path.exists(config):
        with open(config, 'r') as r:
            image_list = json.load(r)
            for key in image_list.keys():
                if key == name:
                    image_list.pop(key)
                    break
        create_master_config(image_list)
    return True


def create_master_config(config=None):
    mconf = app.config['MASTER_CONFIG']

    if config is None:
        config = {}
        image_fold = app.config['IMAGE_FOLDER']
        for image in os.listdir(image_fold):
            if os.path.isdir(os.path.join(image_fold, image)):
                config.setdefault(image, [])
        keys = list(config.keys())
        if keys:
            config['default'] = config[keys[0]]

    if not os.path.exists(mconf):
        if config['default'] is None:
            keys = list(config.keys())
            config['default'] = config[keys[0]]
        with open(mconf, 'w') as w:
            json.dump(config, w, indent=2)
        return True

    with open(mconf, 'r') as r:
        old_conf = json.load(r)
    dir_name = os.path.join(os.path.dirname(mconf))
    new_name = ''.join([os.path.basename(mconf).split('.')[0],
                        str(time.time()).split('.')[0],
                        '.',
                        os.path.basename(mconf).split('.')[1]])
    os.rename(mconf, os.path.join(dir_name, new_name))
    if config['default'] is None:
        config['default'] = old_conf['default']
    with open(mconf, "w") as f:
        json.dump(config, f, indent=2)
    return True


def get_master_config():
    msconf = app.config['MASTER_CONFIG']
    if not os.path.exists(msconf):
        create_master_config()
    with open(msconf, 'r') as r:
        config = json.load(r)

    macs_with_images = {}
    for mac in app.config['MACS']:
        macs_with_images.setdefault(mac, 'default')
    for image in config:
        if image == 'default':
            continue
        for mac in config[image]:
            if mac in macs_with_images:
                macs_with_images[mac] = image
            else:
                macs_with_images.setdefault(mac, image)
        for mac in macs_with_images:
            if not macs_with_images[mac]:
                macs_with_images[mac] = 'default'
    return macs_with_images
