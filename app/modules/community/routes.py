from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.modules.community.forms import CommunityForm
from app.modules.community import community_bp
from app.modules.community.services import CommunityService

community_service = CommunityService()

@community_bp.route('/my-communities', methods=['GET'])
@login_required
def my_communities():
    form = CommunityForm()
    communities = community_service.get_all_by_user(current_user.id)
    return render_template('community/index.html', communities=communities, form=form)

@community_bp.route('/joined-communities', methods=['GET'])
@login_required
def joined_communities():
    form = CommunityForm()
    communities = community_service.get_all_joined_by_user(current_user.id)
    return render_template('community/index.html', communities=communities, form=form)
