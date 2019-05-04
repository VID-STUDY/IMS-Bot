from application.admin import bp
from application.core import channelservice
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from .forms import ChannelForm


@login_required
@bp.route('/channels', methods=['GET', 'HEAD'])
def all_channels():
    channels = channelservice.get_all_channels()
    return render_template('admin/channels.html', title='ТВ-каналы', channels=channels)


@login_required
@bp.route('/channel/<int:channel_id>', method=['GET', 'HEAD', 'POST'])
def concrete_channel(channel_id: int):
    channel_form = ChannelForm()
    if channel_form.validate_on_submit():
        price_files = request.files.getlist('price_files')
        package_offers_files = request.files.getlist('package_offers_files')
        name = channel_form.name.data
        channelservice.update_channel(channel_id, name, price_files, package_offers_files)
        flash('Канал {} успешно изменён'.format(channel_form.name.data), category='success')
        return redirect(url_for('admin.channels'))
    channel = channelservice.get_channel_by_id(channel_id)
    channel_form.name.data = channel.name
    return render_template('admin/channel.html',
                           title='Канал {}'.format(channel.name),
                           form=channel_form,
                           channel=channel)


@login_required
@bp.route('/channel/new', methods=['GET', 'HEAD', 'POST'])
def new_channel():
    channel_form = ChannelForm()
    if channel_form.validate_on_submit():
        price_files = request.files.getlist('price_files')
        package_offers_files = request.files.getlist('package_offers_files')
        name = channel_form.name.data
        channelservice.create_channel(name, price_files, package_offers_files)
        flash('Канал {} успешно создан!'.format(channel_form.name.data), category='success')
        return redirect(url_for('admin.channels'))
    return render_template('admin/new_channel.html', title='Новый канал', form=channel_form)


@login_required
@bp.route('/channel/<int:channel_id>/delete', methods=['POST'])
def delete_channel(channel_id: int):
    channelservice.remove_channel(channel_id)
    flash('Канал удалён', category='success')
    return redirect(url_for('admin.channels'))
