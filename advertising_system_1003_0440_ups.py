# 代码生成时间: 2025-10-03 04:40:47
from bottle import route, run, request, response, template

# 模拟的广告数据存储
ADS = [
    {'id': 1, 'title': 'Ad 1', 'description': 'Advertisement 1', 'status': 'active'},
    {'id': 2, 'title': 'Ad 2', 'description': 'Advertisement 2', 'status': 'inactive'},
    {'id': 3, 'title': 'Ad 3', 'description': 'Advertisement 3', 'status': 'active'},
]

# 首页路由，显示所有广告
@route('/')
def index():
    return template('ads_list', ads=ADS)

# 广告详情路由
@route('/ad/<ad_id:int>')
def show_ad(ad_id):
    ad = next((ad for ad in ADS if ad['id'] == ad_id), None)
    if ad is not None:
        return template('ad_detail', ad=ad)
    else:
        response.status = 404
        return 'Ad not found'

# 创建新广告路由
@route('/new', method='GET')
def new_ad():
    return template('new_ad_form')

@route('/new', method='POST')
def create_ad():
    ad = request.forms.get('ad')
    if ad:
        AD = {
            'id': len(ADS) + 1,
            'title': ad['title'],
            'description': ad['description'],
            'status': ad['status']
        }
        ADS.append(AD)
        return f"Ad {AD['title']} created successfully!"
    else:
        response.status = 400
        return 'Invalid request'

# 更新广告状态路由
@route('/ad/<ad_id:int>/activate', method='PUT')
def activate_ad(ad_id):
    global ADS
    for ad in ADS:
        if ad['id'] == ad_id:
            ad['status'] = 'active'
            break
    return f"Ad {ad_id} activated successfully!"

# 更新广告状态路由
@route('/ad/<ad_id:int>/deactivate', method='PUT')
def deactivate_ad(ad_id):
    global ADS
    for ad in ADS:
        if ad['id'] == ad_id:
            ad['status'] = 'inactive'
            break
    return f"Ad {ad_id} deactivated successfully!"

# 运行Bottle服务
if __name__ == '__main__':
    run(host='localhost', port=8080)


# HTML模板 - ads_list.tpl
# 显示所有广告列表
<ul>
    % for ad in ads:
    <li>{{ad['title']}} - {{ad['description']}} - {{ad['status']}}
        <a href="/ad/{{ad['id']}}">View</a>
    </li>
    % end
</ul>

# HTML模板 - ad_detail.tpl
# 显示广告详情
<p>Ad Title: {{ad['title']}}</p>
<p>Ad Description: {{ad['description']}}</p>
<p>Ad Status: {{ad['status']}}</p>
<a href="/">Back to List</a>

# HTML模板 - new_ad_form.tpl
# 新广告表单
<form action="/new" method="post">
    Title: <input type="text" name="ad[title]"><br>
    Description: <textarea name="ad[description]"></textarea><br>
    Status: <input type="text" name="ad[status]"><br>
    <input type="submit" value="Create Ad">
</form>
