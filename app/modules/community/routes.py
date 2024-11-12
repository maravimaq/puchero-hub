from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.modules.community.models import Community
from app.modules.community.forms import CommunityForm
from app.modules.community import community_bp
from app.modules.community.services import CommunityService

community_service = CommunityService()


@community_bp.route('/my-communities', methods=['GET'])
@login_required
def my_communities():
    form = CommunityForm()
    owned_communities = community_service.get_all_by_user(current_user.id)
    joined_communities = community_service.get_all_joined_by_user(current_user.id)
    all_communities = list({community.id: community for community in owned_communities + joined_communities}.values())

    return render_template('community/index.html', communities=all_communities, form=form)


@community_bp.route('/community/create', methods=['GET', 'POST'])
@login_required
def create_community():
    form = CommunityForm()
    if form.validate_on_submit():
        community = Community(
            name=form.name.data,
            description=form.description.data,
            owner_id=current_user.id
        )

        community.members.append(current_user)

        try:
            db.session.add(community)
            db.session.commit()
            flash('Community created successfully!', 'success')
            return redirect(url_for('community.my_communities'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating community: {str(e)}', 'danger')
            return render_template('community/create.html', form=form)

    return render_template('community/create.html', form=form)


@community_bp.route('/community/edit/<int:community_id>', methods=['GET', 'POST'])
@login_required
def edit_community(community_id):
    community = community_service.get_by_id(community_id)

    if not community or community.owner_id != current_user.id:
        flash('Community not found or you do not have permission to edit it.', 'danger')
        return redirect(url_for('community.my_communities'))

    form = CommunityForm(obj=community)

    if form.validate_on_submit():
        # Usar el método update de BaseService para actualizar la comunidad
        updated_community = community_service.update(
            id=community_id,
            name=form.name.data,
            description=form.description.data
        )

        if updated_community:
            flash('Community updated successfully!', 'success')
            return redirect(url_for('community.my_communities'))
        else:
            flash('Error updating community. Please try again.', 'danger')
            return render_template('community/edit.html', form=form, community=community)

    return render_template('community/edit.html', form=form, community=community)


@community_bp.route('/community/delete/<int:community_id>', methods=['POST'])
@login_required
def delete_community(community_id):
    community = community_service.get_by_id(community_id)

    # Verificar si la comunidad existe y si el usuario es el propietario
    if not community or community.owner_id != current_user.id:
        flash('Community not found or you do not have permission to delete it.', 'danger')
        return redirect(url_for('community.my_communities'))

    try:
        community_service.delete(community_id)
        flash('Community deleted successfully!', 'success')
        return redirect(url_for('community.my_communities'))
    except Exception as e:
        flash(f'Error deleting community: {str(e)}', 'danger')
        return redirect(url_for('community.my_communities'))


@community_bp.route('/community/<int:community_id>', methods=['GET'])
@login_required
def show_community(community_id):
    community = community_service.get_by_id(community_id)

    if not community:
        flash('Community not found.', 'danger')
        return redirect(url_for('community.my_communities'))

    members = community_service.get_members_by_id(community_id)
    return render_template('community/show.html', community=community, members=members)
