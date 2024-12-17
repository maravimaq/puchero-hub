from flask import render_template, request, jsonify
from app.modules.explore import explore_bp
from app.modules.explore.forms import ExploreForm
from app.modules.explore.services import ExploreService


@explore_bp.route('/explore', methods=['GET', 'POST'])
def index():
    form = ExploreForm()
    if request.method == 'GET':
        query = request.args.get('query', '')
        datasets = ExploreService().filter()  # Load all datasets initially
        return render_template('explore/index.html',
                               form=form, query=query, datasets=[dataset.to_dict() for dataset in datasets])

    if request.method == 'POST':
        criteria = request.get_json()
        datasets = ExploreService().filter(**criteria)
        return jsonify([dataset.to_dict() for dataset in datasets])
    return render_template('explore/index.html', form=form)
