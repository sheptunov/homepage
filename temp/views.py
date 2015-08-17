# -*- coding: utf-8 -*-
from django.core.paginator import EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, RequestContext, render_to_response, get_object_or_404, get_list_or_404, redirect, HttpResponse
# from django.utils.translation import get_language

from . forms import SearchFormLouer
from . models import Ad, TYPE_OPTIONS, CATEGORY_OPTIONS



# custom func
def i(val): # safe typeToInt
    try:
        return int(val)
    except ValueError:
        return ''

def getPositiveIntVal(val):
    if not isinstance(val, int):
        val = i(val)

    if val > 0:
        return val
    else:
        return 1


def getPageIntVal(page = {}):
    if isinstance(page, int):
        return page if page and page > 0 else 0
    else:
        if page.get('page', False):
            return i(page.get('page', 1)) if i(page.get('page', 1)) > 0 else 1
        else:
            return 1
def getPerageIntVal(page = {}):
    if isinstance(page, int):
        return page.get('perpage', False) if page.get('perpage', False) and page.get('perpage', False) > 30 else 30
    else:
        if page.get('perpage', 30):
            return i(page.get('perpage', 30))
        else:
            return 30

def m(numList):         # [1,2,3]
    s = map(str, numList)   # ['1','2','3']
    s = ''.join(s)          # '123'
    s = int(s)              # 123
    return s

def normalize(s):
    '''
    This function removes | in the end or at the beginning of the string
    :param s:
    :return:
    '''
    if isinstance(s, str) or isinstance(s, unicode):
        s = s.strip()
        if s[0] == '|' and len(s):
            s = s[1:]
        if s[-1:] == '|' and len(s):
            s = s[:-1]
    return s
# Create your views here.
# form new chpu url
def removeLeadOrTrailingSeparator(url='', separator='-'):
    if separator in url:
        if url[0] == separator:
            url = url[1:]
        if url[-1:] == separator:
            url = url[:-1]
    return url


def indexPage(request, page=''):
    page = 0
    if 'page' in request.GET:
        page = request.GET.get('page', False)
    if not page:
        page = 1
    context = {}
    total = 0
    if 'total' in request.session:
        total = request.session.get('total', False)
    # get total ad count
    if not total:
        total = Ad.objects.filter(is_published=1).count()
        request.session['total'] = total
    context['total'] = total

    type = request.session.get('type', 'louer')
    category = request.session.get('category', '').lower()

    if 'address' in request.session:
        address = request.session['address']
    else:
        address = 'Lausanne'
        request.session['address'] = 'Lausanne'


    context['type'] = type
    context['category'] = category
    context['address'] = address

    formDict = {
        'type': type,
        'category': category,
        'address': address,
        }
    form = SearchFormLouer(formDict)
    context["form"] = form

#    paginate_by = '10'
#    object_list = get_list_or_404(Ad)
#    context["paginator"] = Paginator(object_list, paginate_by)
#    context["object_list"] = context["paginator"].page(page)

    if 'last_visited' in request.session:
        visited = request.session['last_visited']
        context['last_visited_id'] = []
        for item in visited:
            context['last_visited_id'].append(i(item))
        try:
            context['last_visited_id']=context.get('last_visited_id', False)[-5:]
        except TypeError:
            pass
        context['last_visited'] = Ad.objects.filter(id__in=context['last_visited_id'])

    if request.GET.get('new'):
        return render(request, 'front/new_index.html', context)

    return render(request, 'front/ad_index.html', context)


def detailPage(request, pk=''):
    '''
    Detail page view function
    :param request:
    :param pk:
    :return:
    '''

    object = get_object_or_404(Ad.with_expired, pk=pk)
    if not object.is_published:
        return render_to_response('front/ad_detail_expired.html', {}, context_instance=RequestContext(request))

    perpage = 30
    context = {}
    filtersInitial = {}
    # get total ad count
    total = request.session.get('total', False)
    if not total:
        total = Ad.objects.filter(is_published=1).count()
        request.session['total'] = total
    # total = Ad.objects.count()
    context['total'] = total
    type = ''
    category = ''
    categoryTags = []
    categoryTitle = ''
    categoryQuery = ''
    categoryUrl = ''
    # address
    address = ''
    addressTags = []
    addressTitle = ''
    addressQuery = ''
    addressUrl = ''
    page = 0
    order_field = 'date'
    order_direction = 'desc'
    furnished = False


    # if we querying next page
    if 'page' in request.session:
        page = request.session.get('page', False)
    if not page:
        page = 1

    # if 'type' in request.session:
    #    type = request.session.get('type', False)
    # else:
    type = object.type
    request.session['type'] = object.type.lower()

    # if 'category' in request.session:
    #    category = request.session.get('category', False)
    # else:
    category = object.category
    request.session['category'] = object.category.lower()

    if 'address' in request.session:
        address = request.session.get('address', False)
    else:
        address = object.city # adv address


    type = type.lower()
    category = category.lower()
    address = address.lower()
    # check do we have multiple params in address
    multiple_address = False
    if address:
        multiple_address = address.split(',')
        if len(multiple_address) > 1:
            multiple_address = [item.strip() for item in multiple_address if item]

    # write viewed items in session
    context['contact_summary'] = object.contact_summary
    visited = request.session.get('last_visited', [])
    if pk and pk not in visited:
        visited.append(pk)

        # increase views_count if for unique views
        object.views_count += 1
        object.save()
    request.session['last_visited'] = visited

    # write search history in session
    if 'search_history' not in request.session:
        request.session['search_history'] = []

    visited_id_list = ''
    last_search_url = request.session.get('last_search_url', False)
    if 'last_visited' in request.session:
        visited = request.session.get('last_visited', False)
        visited_id_list = []
        for item in visited:
            visited_id_list.append(i(item))

        # get last five items
        try:
            visited_id_list = visited_id_list[-5:]
        except TypeError:
            pass

        if visited_id_list:
            context['visited_items'] = Ad.objects.filter(id__in=visited_id_list)
            # context['len'] = Ad.objects.filter(id__in=visited_id_list)[0]


    # take GET search params and push it into form
    price_min = False
    if 'price_min' in request.session:
        price_min = request.session.get('price_min', False)
    if price_min:
        request.session['price_min'] = price_min
        context['price_min'] = price_min

    price_max = False
    if 'price_max' in request.session:
        price_max = request.session.get('price_max', False)
    if price_max:
        request.session['price_max'] = price_max
        context['price_max'] = price_max
    # area
    area_min = False
    if 'area_min' in request.session:
        area_min = request.session.get('area_min', False)
    if area_min:
        request.session['area_min'] = area_min
        context['area_min'] = area_min

    area_max = False
    if 'area_max' in request.session:
        area_max = request.session.get('area_max', False)
    if area_max:
        request.session['area_max'] = area_max
        context['area_max'] = area_max
    # rooms
    rooms_min = False
    if 'rooms_min' in request.session:
        rooms_min = request.session.get('rooms_min', False)
    if rooms_min:
        request.session['rooms_min'] = rooms_min
        context['rooms_min'] = rooms_min

    rooms_max = False
    if 'rooms_max' in request.session:
        rooms_max = request.session.get('rooms_max', False)
    if rooms_max:
        request.session['rooms_max'] = rooms_max
        context['rooms_max'] = rooms_max

    # is_furnished
    furnished = True if request.session.get('furnished', False) == '1' else False

    #search page url
    context['search_page_url'] = request.session.get('search_page_url', False)

    # check order queryset params
    if 'order_field' in request.session:
        order_field = request.session.get('order_field', False)
    if 'order_direction' in request.session:
        order_direction = request.session.get('order_direction', False)

    # check per page queryset limits
    if 'perpage' in request.session:
        perpage = request.session.get('perpage', False)

    request.session['price_filter'] = False
    request.session['area_filter'] = False
    request.session['rooms_filter'] = False
    if price_min or price_max:
        request.session['price_filter'] = True
    if area_min or area_max:
        request.session['area_filter'] = True
    if rooms_min or rooms_max:
        request.session['rooms_filter'] = True

    # initial filters
    filtersInitial = request.session.get('filtersInitial')
    if isinstance(address, list):
            addressTags = address
            addressTitle = '%s '.join(addressTags)
            addressQuery = '|'.join(addressTags)
            addressUrl = '-'.join(addressTags)
    else:
        if '|' in address:
            addressTags = address.split('|')
            addressTags = [item.strip() for item in addressTags]
        #if ',' in address:
        #    addressTags = address.split(',')
        #    addressTags = [item.strip() for item in addressTags]
        addressTitle = address.title()
        addressTags = address.split()
        addressQuery = address
        addressUrl = '%s-' % address
    context['addressTitle'] = addressTitle
    context['addressTags'] = addressTags
    context['addressQuery'] = addressQuery
    context['addressUrl'] = addressUrl

    if isinstance(category, list):
        categoryTags = category
        categoryTitle = ', '.join(categoryTags)
        categoryQuery = '|'.join(categoryTags)
        categoryUrl = '-et-'.join(categoryTags)
    else:
        if '|' in category:
            categoryTags = category.split('|')
            categoryTags = [item.strip() for item in categoryTags]
        if ',' in category:
            categoryTags = category.split(',')
            categoryTags = [item.strip() for item in categoryTags]
        categoryTitle = category.title()
        categoryTags = category.split()
        categoryQuery = category
        categoryUrl = '%s-' % category

    context['categoryTitle'] = categoryTitle
    context['categoryTags'] = categoryTags
    context['categoryQuery'] = categoryQuery
    context['categoryUrl'] = categoryUrl


    typeTitle = type.title()
    typeTags = type.split()
    typeQuery = type
    typeUrl = '%s-' % type

    context['typeTitle'] = typeTitle
    context['typeTags'] = typeTags
    context['typeQuery'] = typeQuery
    context['typeUrl'] = typeUrl

    # populate tags data
    address_tags = {
        'class': 'address',
        'value': addressTags if multiple_address else address
    }
    price_tags = {
        'class':'price',
        'from': price_min,
        'to': price_max,
        }
    area_tags = {
        'class':'area',
        'from': area_min,
        'to': area_max,
        }
    rooms_tags = {
        'class':'rooms',
        'from': rooms_min,
        'to': rooms_max,
        }
    # create huge dictionary
    tags = {
        'address': address_tags,
        'furnished': True if furnished else False,
        'price': price_tags if request.session.get('price_filter', False) else False,
        'area': area_tags if request.session.get('area_filter', False) else False,
        'rooms': rooms_tags if request.session.get('rooms_filter', False) else False,
        }

    context['filtersInitial'] = filtersInitial

    # create for class object and populate it
    formDict = {
        'type': type,
        'category': category,
        'address': address,
        # additional params
        'price_min': price_min if price_min else 0,
        'price_max': price_max if price_max else 0,
        'area_min': area_min if area_min else 0,
        'area_max': area_max if area_max else 0,
        'rooms_min': rooms_min if rooms_min else '0',
        'rooms_max': rooms_max if rooms_max else '0',
        'furnished': furnished,
        # order
        'order_field': order_field,
        'order_direction': order_direction,
        # perpage
        'perpage': perpage,
        }
    form = SearchFormLouer(formDict)
    if form.is_valid():
        #form.type._initial = type
        context['formStatus'] = 'valid'
        context['form'] = form
        request.session['last_search_url'] = request.build_absolute_uri()
        # build context
        context["type"] = type
        context["category"] = category
        context["address"] = address
        context["tags"] = tags
        context["page"] = i(page)
        context["page_url"] = request.build_absolute_uri()
        context["search_history"] = request.session.get('search_history', False)
        context['order_field'] = order_field
        context['order_direction'] = order_direction
        context['perpage'] = perpage
        context['furnished'] = furnished
        context['template_name'] = 'front/ad_detail.html'
        context['object'] = object
        context['last_search_url'] = last_search_url
        context['last_visited_id_list'] = visited_id_list
        return render(request, context['template_name'], context)
    else:
        context['formStatus'] = formDict
        context["type"] = type
        context["category"] = category
        context["address"] = address
        context["tags"] = tags
        context["page"] = i(page)
        context["page_url"] = request.build_absolute_uri()
        context["search_history"] = request.session.get('search_history', False)
        context['order_field'] = order_field
        context['order_direction'] = order_direction
        context['perpage'] = perpage
        context['furnished'] = furnished
        context['template_name'] = 'front/ad_detail.html'
        context['object'] = object
        context['last_search_url'] = last_search_url
        context['last_visited_id_list'] = visited_id_list
        return render(request, context['template_name'], context)

def searchByParam(request, queryParam='', typeParam=False, categoryParam=False, multipleCategoryParam=False, cityParam=False, addressParam=False, roomsParam=False, priceParam=False, areaParam=False, furnishedParam=False, pageParam=False, orderParam=False, optionsParam=False):
    '''
    Search queryset by param function
    :param request:
    :param chpu:
    :return:
    '''
    context = {}
    filtersInitial = {}
    # get total ad count
    total = Ad.objects.filter(is_published=1).count()
    context['total'] = total
    type = ''
    # category
    category = ''
    categoryTags = []
    categoryTitle = ''
    categoryQuery = ''
    categoryUrl = ''
    # address
    address = ''
    addressTags = []
    addressTitle = ''
    addressQuery = ''
    addressUrl = ''
    # order
    order = {'order_field':'date', "order_direction": "desc"}
    order_field = 'date'
    order_direction = 'desc'
    # page
    page = {'page':1, "perpage": 30}
    type = typeParam if typeParam else type
    category = categoryParam if categoryParam else category
    address = addressParam if addressParam else address
    request.session['page'] = getPageIntVal(page)
    request.session['perpage'] = getPerageIntVal(page)
    # assign vars to view arguments
    #address = cityParam if cityParam else address
    # convert all params to lower register
    type = type.lower()
    category = category.lower()
    address = address.lower()
    # check do we have multiple params in address
    multiple_address = False
    if address:
        multiple_address = address.split(',')
        if len(multiple_address) > 1:
            multiple_address = [item.strip() for item in multiple_address if item]
    # multiple category
    multipleCategory = False
    if category:
        multipleCategory = category.split(',')
        if len(multipleCategory) > 1:
            multipleCategory = [item.strip() for item in multipleCategory if item]


    # check do we have additional search filters
    # price
    price_min = False
    price_max = False
    # area
    area_min = False
    area_max = False
    # rooms
    rooms_min = False
    rooms_max = False
    # furnished
    furnished = False
    # options
    options = False

    # translate function parameters to function variables"loading
    # price
    price_min = priceParam['min'] if priceParam and priceParam.get('min', False) else price_min
    price_max = priceParam['max'] if priceParam and priceParam.get('max', False) else price_max
    # area
    area_min = areaParam['min'] if areaParam and areaParam.get('min', False) else area_min
    area_max = areaParam['max'] if areaParam and areaParam.get('max', False) else area_max
    # rooms
    rooms_min = roomsParam['min'] if roomsParam and roomsParam.get('min', False) else rooms_min
    rooms_max = roomsParam['max'] if roomsParam and roomsParam.get('max', False) else rooms_max
    # meuble
    furnished = str(furnishedParam) if furnishedParam else furnished
    # order filters
    order['order_field'] = orderParam['order_field'] if orderParam.get('order_field', False) else order.get('order_field', 'date')
    order['order_direction'] = orderParam['order_direction'] if orderParam.get('order_direction', False) else order.get('order_direction', 'desc')
    #pagination filters
    page['page'] = pageParam.get('page', False) if pageParam.get('page', False) else getPageIntVal(page)
    page['perpage'] = pageParam['perpage'] if pageParam.get('perpage', False) else getPerageIntVal(page)
    options = optionsParam if optionsParam else options

    # is_furnished
    request.session['furnished'] = False
    furnished = i(furnished) if furnished else False
    if multiple_address:
        s = ', '.join(multiple_address).strip()
        s = normalize(s)
        addressTags = s.replace(' ', '').replace("'",'').replace("-", "")
        address = addressTags
        addressTags = addressTags.replace(",",'|')
        aTags = addressTags.split('|')
        #query = '@type ' + type + ' @category ' + category + ' @city ' + addressTags
    categoryTags = ''
    categoryQuery = ''
    categoryTitle = ', '.join([item.title() for item in categoryTags])
    if multipleCategory:
        categoryQuery = category
        categoryTags = category.split('|')
        categoryList = categoryTags
        categoryTitle = ', '.join(categoryTags)
        context['debug-category-tabs'] = categoryTags
        #category = ', '.join(categoryTags)
        #if multiple_address:
        #    query = '@category ' + category + ' @city ' + addressTags

    if isinstance(address, list):
        addressTags = address
        addressTitle = '%s '.join(addressTags)
        addressQuery = '|'.join(addressTags)
        addressUrl = '-'.join(addressTags)
    else:
        if '|' in address:
            addressTags = address.split('|')
            addressTags = [item.strip() for item in addressTags]
        if ',' in address:
            addressTags = address.split(',')
            addressTags = [item.strip() for item in addressTags]
        addressTitle = address.title()
        addressQuery = '|'.join(addressTags)
        addressUrl = '-'.join(addressTags)
    context['addressTitle'] = addressTitle
    context['addressTags'] = addressTags
    context['addressQuery'] = addressQuery
    context['addressUrl'] = addressUrl

    if isinstance(category, list):
        categoryTags = category
        categoryTitle = ', '.join(categoryTags)
        categoryQuery = '|'.join(categoryTags)
        categoryUrl = '-et-'.join(categoryTags)
    else:
        if '|' in category:
            categoryTags = category.split('|')
            categoryTags = [item.strip() for item in categoryTags]
        if ',' in category:
            categoryTags = category.split(',')
            categoryTags = [item.strip() for item in categoryTags]
        categoryTitle = categoryTitle.title()
        categoryQuery = '|'.join(categoryTags)
        categoryUrl = '-'.join(categoryTags)

    context['categoryTitle'] = categoryTitle
    context['categoryTags'] = categoryTags
    context['categoryQuery'] = categoryQuery
    context['categoryUrl'] = categoryUrl

    addressTags = addressTags if addressTags else address
    categoryTags = categoryTags if categoryTags else category

    query = ''
    if type:
        query = query + ' @type ' + type
    if category:
        query = query + ' @category ' + categoryQuery
    if address:
        query = query + ' @city ' + address
    #query = '@type ' + type + ' @category ' + category + ' @city ' + addressTags

    request.session['aDEBUG'] = [type, addressQuery, categoryQuery, categoryTags, categoryTags, categoryQuery]
    #request.session.flush

    #request.session['tg111'] = category or type or address
    # Do sphinx search
    #
    # if we don't have additional parameters
    results = Ad.search.query(query)
    # modify query and add additional parameters like price, rooms and area
    # clear filter flags
    request.session['price_filter'] = False
    request.session['area_filter'] = False
    request.session['rooms_filter'] = False
    resultsCount = Ad.search.query(query).count()
    if resultsCount:
        # price
        filtersInitial['price_min'] = price_min if price_min else 0
        filtersInitial['price_max'] = price_max if price_max else 0
        # area
        filtersInitial['area_min'] = area_min if area_min else 0
        filtersInitial['area_max'] = area_max if area_max else 0
        # rooms
        filtersInitial['rooms_min'] = rooms_min if rooms_min else 0
        filtersInitial['rooms_max'] = rooms_max if rooms_max else 0
        # order
        #order_field = order.get('order_field', 'date')
        #order_direction = order.get('order_direction', 'desc')
        context['order_field'] = order.get('order_field', 'date')
        context['order_direction'] = order.get('order_direction', 'date')
        filtersInitial['order_field'] = order.get('order_field', 'date')
        filtersInitial['order_direction'] = order.get('order_direction', 'desc')
        # page
        page_perpage = False
        page_perpage = getPerageIntVal(page)
        if 'page_perpage' in request.GET:
            page_perpage = request.GET.get('page_perpage', False)
        if 'page_perpage' in request.session:
            request.session['page_perpage'] = getPerageIntVal(page)
        page_page = False
        page_page = getPageIntVal(page)
        if 'page_page' in request.GET:
            page_page = request.GET.get('page_page', False)
        if 'page_page' in request.session:
            request.session['page_page'] = getPageIntVal(page)

        filtersInitial['page_page'] = page_page
        filtersInitial['page_perpage'] = page_perpage
        request.session['page_page'] =page_page
        request.session['page_perpage'] =page_perpage
        request.session['filtersInitial'] = filtersInitial


    # filter by price
    if price_min or price_max:
        request.session['price_filter'] = True
        # [1..2]
        if price_min and price_max:
            results = Ad.search.query(query).filter(price__gte=i(price_min)).filter(price__lte=i(price_max))

            # [1 .. x]
        elif price_min and not price_max:
            results = Ad.search.query(query).filter(price__gte=i(price_min))
            # [x .. 2]
        elif price_max and not price_min:
            results = Ad.search.query(query).filter(price__lte=i(price_max))
    # filter by area
    if area_min or area_max:
        request.session['area_filter'] = True
        # [1..2]
        if area_min and area_max:
            results = Ad.search.query(query).filter(area__gte=area_min).filter(area__lte=area_max)
            # [1 .. x]
        elif area_min and not area_max:
            results = Ad.search.query(query).filter(area__gte=area_min)
            # [x .. 2]
        elif area_max and not area_min:
            results = Ad.search.query(query).filter(area__lte=area_max)
    # filter by rooms
    if rooms_min or rooms_max:
        request.session['rooms_filter'] = True
        # [1..2]
        if rooms_min and rooms_max:
            results = Ad.search.query(query).filter(rooms__gte=float(rooms_min)).filter(rooms__lte=float(rooms_max))
            # [1 .. x]
        elif rooms_min and not rooms_max:
            results = Ad.search.query(query).filter(rooms__gte=float(rooms_min))
            # [x .. 2]
        elif rooms_max and not rooms_min:
            results = Ad.search.query(query).filter(rooms__lte=float(rooms_max))
    # is furnished
    if furnished:
        results = results.filter(is_furnished=furnished)

    # order filters
    if order['order_field'] == 'date':
        if order['order_direction'] == 'desc':
            results = results.order_by('-date_created')
        else:
            results = results.order_by('date_created')
    elif order['order_field'] == 'price':
        if order['order_direction'] == 'desc':
            results = results.order_by('-price')
        else:
            results = results.order_by('price')
    elif order['order_field'] == 'rooms':
        if order['order_direction'] == 'desc':
            results = results.order_by('-rooms')
        else:
            results = results.order_by('rooms')
    elif order['order_field'] == 'area':
        if order['order_direction'] == 'desc':
            results = results.order_by('-area')
        else:
            results = results.order_by('area')
    else:
        results = results.order_by('date_created')


    # ? or &
    have_filters = request.session.get('price_filter', False) or request.session.get('area_filter', False) or request.session.get('rooms_filter', False)

    chpu_url = ''
    # category
    if category:
        if categoryTags.__len__()>1:
            arr = '-et-'.join(categoryTags)
            chpu_url = chpu_url + arr
            #for ctg in categoryTags:
            #    chpu_url = chpu_url + ctg + '-et-'
        else:
            chpu_url = '-%s-' % category
        # type
    if type:
        chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-a-%s-' % type
        # address
    if address:
        aTags = ''
        if isinstance(addressTags, list):
            aTags = addressTags
            aTags = [item.strip() for item in aTags]
        if "|" in addressTags:
            aTags = addressTags.split('|')
            aTags = [item.strip() for item in aTags]
        if "," in addressTags:
            aTags = addressTags.split(',')
            aTags = [item.strip() for item in aTags]
        if aTags.__len__()>1:
            for item in aTags:
                chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-%s-' % item
        else:
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-%s-' % address
        # price
    if price_min or price_max:
        if price_min:
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-prix-de-%s-' % price_min
        if price_max:
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-prix-a-%s-' % price_max
        # area
    if area_min or area_max:
        if area_min:
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-area-de-%s-' % area_min
        if area_max:
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-area-a-%s-' % area_max
        # rooms
    if rooms_min or rooms_max:
        if rooms_min:
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-pieces-de-%s-' % rooms_min
        if rooms_max:
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-pieces-a-%s-' % rooms_max
        # order
    if order_field or order_direction:
        if order_field:
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-order-by-%s-' % order_field
        if order_direction:
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-order-direction-%s-' % order_direction
        # page
    if getPageIntVal(page) or getPerageIntVal(page):
        if getPageIntVal(page):
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-page-%s-' % getPageIntVal(page)
        if getPerageIntVal(page):
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-perpage-%s' % getPerageIntVal(page)

        # furnished
    if furnished:
        chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-meuble'

    if ',' in chpu_url:
        chpu_url = chpu_url.replace(',','-')
    if '|' in chpu_url:
        chpu_url = chpu_url.replace('|','-')
    context['chpu_url'] = chpu_url
    request.session['chpu_url'] = chpu_url
    # write search history in session
    # request.session['search_history'] = []
    #request.session['search_history_query_list'] = []
    if 'search_history_query_list' not in request.session:
        request.session['search_history_query_list'] = []
    if 'search_history' not in request.session:
        request.session['search_history'] = []
    search_history_query_list = request.session.get('search_history_query_list', False)
    search_history = request.session.get('search_history', False)
    if query and query not in search_history_query_list:
        d = {"query": query, "type": type, "category": category, "address": address, "url": request.build_absolute_uri()}
        search_history.append(d)
        search_history_query_list.append(query)

    # define page title
    titleType = 'Rent'
    if type.lower() == 'louer':
        titleType = 'Rent'
    if type.lower() == 'acheter':
        titleType = 'Buy'
    titleAddress = address.title() if address else 'VD'
    if categoryTitle:
        categoryTitle = categoryTitle
    else:
        x = category.replace('|', ', ')
        x = [item.title() for item in x]
    #categoryTitle = categoryTitle if categoryTitle else category.replace('|', ', ')
    context['title'] = '%s for %s a %s' % (category if not categoryTitle else categoryTitle, titleType, titleAddress)
    context['category_title'] = categoryTitle

    resultsCount = results.count()
    # create tags var
    address_tags = {
        'class': 'address',
        'value': multiple_address if multiple_address else address
    }
    price_tags = {
        'class':'price',
        'from': price_min,
        'to': price_max,
        }
    area_tags = {
        'class':'area',
        'from': area_min,
        'to': area_max,
        }
    rooms_tags = {
        'class':'rooms',
        'from': rooms_min,
        'to': rooms_max,
        }
    # create huge dictionary
    tags = {
        'type': type,
        'category': categoryTags if categoryTags else category,
        'address': address_tags,
        'furnished': True if furnished else False,
        'price': price_tags if request.session.get('price_filter', False) else False,
        'area': area_tags if request.session.get('area_filter', False) else False,
        'rooms': rooms_tags if request.session.get('rooms_filter', False) else False,
        }

    context["page_url"] = request.build_absolute_uri()
    request.session["search_page_url"] = context["page_url"]
    # create for class object and populate it
    formDict = {
        'type': type,
        'category': category,
        'address': address,
        # additional params
        'price_min': price_min,
        'price_max': price_max,
        'area_min': area_min,
        'area_max': area_max,
        'rooms_min': rooms_min,
        'rooms_max': rooms_max,
        'furnished': furnished,
        # order
        'order_field': order['order_field'],
        'order_direction': order['order_direction'],
        # perpage
        'perpage': getPerageIntVal(page),
        'page': getPageIntVal(page),
        }
    context["formDict"] = formDict
    form = SearchFormLouer(formDict)
    canonicalLink = ''
    if (category or type or address) and (furnished or price_min or price_max or area_min or area_max or rooms_min or rooms_max):
        if category:
            canonicalLink = canonicalLink + '%s-' % categoryUrl
        if type:
            canonicalLink = canonicalLink + '%s-' % type
        if address:
            canonicalLink = canonicalLink + '%s-' % addressUrl
        canonicalLink = canonicalLink[:-1] if canonicalLink[-1:] == '-' else canonicalLink
    request.session['canonicalLink'] = canonicalLink
    context['canonicalLink'] = canonicalLink

    if form.is_valid():
        #form.type._initial = type
        context['form'] = form
        request.session['search_history'] = search_history[-5:]
        request.session['search_history_query_list'] = search_history_query_list
        request.session['last_search_url'] = request.build_absolute_uri()
        # build context
        context["pageInt"] = getPageIntVal(page)
        context['filtersInitial'] = filtersInitial
        context["paginator"] = Paginator(results, getPerageIntVal())
        context["results_count"] = resultsCount
        context["type"] = type
        context["category"] = category
        context["address"] = address
        context["tags"] = tags
        context["query"] = query
        context["debug-page"] = getPageIntVal(page)
        context["object_list"] = context["paginator"].page(getPageIntVal(page))
        # get paginator list range
        debug = ''
        limit = 5
        context['order_field'] = formDict.get('order_field', 'date')
        context['order_direction'] = formDict.get('order_direction', 'desc')
        pagelist = context['paginator'].page_range
        maxPage = m(pagelist[-1:])
        if page.get('page', 1) == pagelist[0]:
            request.session['gotcha'] = 'gotcha'
            pagelist = pagelist[:limit]
        elif page.get('page', 1) == maxPage:
            request.session['gotcha'] = 'gotcha'
            pagelist = pagelist[-limit:]
        else:
            if context["object_list"].has_previous():
                leftpos = getPageIntVal(page)-3 if getPageIntVal(page)-3 > 0 else 0
                rightpos = limit+getPageIntVal(page)-3 if getPageIntVal(page)+2 < maxPage else maxPage
                if not leftpos:
                    rightpos += 1
                if rightpos == maxPage and not getPageIntVal(page)+2 == maxPage:
                    leftpos -= 1
                    #pass
                pagelist = pagelist[leftpos:rightpos]
                debug = "l %s, r %s, %s, limit+page-3 %s" % (leftpos, rightpos, getPageIntVal(page)+2, limit+getPageIntVal(page)-3)
                request.session['pagination-debug'] = debug
            else:
                if context["object_list"].has_next():
                    leftpos = getPageIntVal(page)+3 if getPageIntVal(page) > 0 else 0
                    rightpos = limit+getPageIntVal(page) if limit+getPageIntVal(page)+3 < pagelist[-1:] else pagelist[-1:]
                    pagelist = pagelist[leftpos:rightpos]
                    debug = "leftpos %s, rightpos %s, page+2 %s, limit+page-3 %s" % (leftpos, rightpos, getPageIntVal(page)+2, limit+getPageIntVal(page)-3)
                request.session['pagination-debug'] = debug

        context["pagelist"] = pagelist
        context['maxpage'] = getPageIntVal()
        context["page"] = getPageIntVal(page)
        context["search_history"] = request.session.get('search_history', False)
        context["have_filters"] = have_filters
        #context['order_field'] = order['order_field']
        #context['order_direction'] = order['order_direction']
        context['perpage'] = getPerageIntVal(page)
        context['furnished'] = furnished
        return render_to_response('front/ad_search.html', context, context_instance=RequestContext(request))
    else:
        form = SearchFormLouer()
        context['form'] = form
        request.session['search_history'] = search_history[-5:]
        request.session['search_history_query_list'] = search_history_query_list
        # build context
        context["pageInt"] = getPageIntVal(page)
        context['filtersInitial'] = filtersInitial
        context["paginator"] = Paginator(results, getPerageIntVal(page))
        context["results_count"] = resultsCount
        context["type"] = type
        context["category"] = category
        context["address"] = address
        context["tags"] = tags
        context["query"] = query
        request.session['chat'] = getPageIntVal(page)
        context["object_list"] = context["paginator"].page(getPageIntVal(page))
        # get paginator list range
        limit = 5
        pagelist = context['paginator'].page_range
        maxPage = m(pagelist[-1:])
        if page.get('page', 1) == pagelist[0]:
            pagelist = pagelist[:limit]
        elif page.get('page', 1) == maxPage:
            pagelist = pagelist[-limit:]
        else:
            if context["object_list"].has_previous():
                leftpos = getPageIntVal(page)-3 if getPageIntVal(page)-3 > 0 else 0
                rightpos = limit+getPageIntVal(page)-3 if getPageIntVal(page)+2 < maxPage else maxPage
                if not leftpos:
                    rightpos += 1
                if rightpos == maxPage and not getPageIntVal(page)+2 == maxPage:
                    leftpos -= 1
                    #pass
                pagelist = pagelist[leftpos:rightpos]
                debug = "l %s, r %s, %s, limit+page-3 %s" % (leftpos, rightpos, getPageIntVal(page)+2, limit+getPageIntVal(page)-3)
            else:
                if context["object_list"].has_next():
                    leftpos = getPageIntVal(page)+3 if getPageIntVal(page) > 0 else 0
                    rightpos = limit+getPageIntVal(page) if limit+page_page+3 < pagelist[-1:] else pagelist[-1:]
                    pagelist = pagelist[leftpos:rightpos]

        page_page = getPageIntVal(page)
        context["pagelist"] = pagelist
        context["page"] = page_page
        context["search_history"] = request.session.get('search_history', False)
        context["have_filters"] = have_filters
        context["var_prefix"] = '&' if have_filters else '?'
        #context['order_field'] = order_field
        #context['order_direction'] = order.get('order_direction', False)
        context['perpage'] = page.get('perpage', 30)
        context['furnished'] = furnished
        #request.session.flush()
        #request.session['context'] = context
        return render_to_response('front/ad_search.html', context, context_instance=RequestContext(request))

def search(request, chpu=False):
    '''
    Search page view function
    :param request:f
    :param query:
    :return:
    '''
    perpage = 30
    context = {}
    order = {'order_field':'date', "order_direction": "desc"}
    order_field = 'date'
    order_direction = 'desc'
    page = 1
    #page = {'page': 1, "perpage": 30}
    #page_page = ''
    #page_perpage = ''
    filtersInitial = {}
    # get total ad count
    total = request.session.get('total', False)
    if not total:
        total = Ad.objects.filter(is_published=1).count()
        request.session['total'] = total
    #total = Ad.objects.count()
    context['total'] = total
    type = 'louer'
    category = ''
    address = ''
    addressTags = []
    addressTitle = ''
    addressQuery = ''
    addressUrl = ''
    furnished = False
    # if we querying next page

    if 'type' in request.GET:
        type = request.GET.get('type', False)
        request.session['type'] = type
    if 'category' in request.GET:
        category = request.GET.get('category', False)
        request.session['category'] = category
    if 'address' in request.GET:
        address = request.GET.get('address', False)
        request.session['address'] = address
    # address
    if isinstance(address, list):
        addressTags = address
        addressTitle = ', '.join(addressTags)
        addressQuery = '|'.join(addressTags)
        addressUrl = '-'.join(addressTags)
    else:
        if '|' in address:
            addressTags = address.split('|')
            addressTags = [item.strip() for item in addressTags]
        if ',' in address:
            addressTags = address.split(',')
            addressTags = [item.strip() for item in addressTags]
        addressTitle = address.title()
        addressQuery = '|'.join(addressTags)
        addressUrl = addressTags
    request.session['addressTitle'] = addressTitle
    request.session['addressTags'] = addressTags
    request.session['addressQuery'] = addressQuery
    request.session['addressUrl'] = addressUrl

    # convert all params to lower register
    type = type.lower()
    category = category.lower()
    address = address.lower()
    # check do we have multiple params in address
    multiple_address = False
    if address:
        multiple_address = address.split(',')
        if len(multiple_address) > 1:
            multiple_address = [item.strip() for item in multiple_address if item]

    # check do we have additional search filters
    # price
    price_min = False
    if 'price_min' in request.GET:
        price_min = request.GET.get('price_min', False)
    if price_min or 'price_min' in request.session:
        request.session['price_min'] = price_min
        context['price_min'] = price_min

    price_max = False
    if 'price_max' in request.GET:
        price_max = request.GET.get('price_max', False)
    if price_max or 'price_max' in request.session:
        request.session['price_max'] = price_max
        context['price_max'] = price_max
    # area
    area_min = False
    if 'area_min' in request.GET:
        area_min = request.GET.get('area_min', False)
    if area_min or 'area_min' in request.session:
        request.session['area_min'] = area_min
        context['area_min'] = area_min

    area_max = False
    if 'area_max' in request.GET:
        area_max = request.GET.get('area_max', False)
    if area_max or 'area_max' in request.session:
        request.session['area_max'] = area_max
        context['area_max'] = area_max
    # rooms
    rooms_min = False
    if 'rooms_min' in request.GET:
        rooms_min = request.GET.get('rooms_min', False)
    if rooms_min or 'rooms_min' in request.session:
        request.session['rooms_min'] = rooms_min
        context['rooms_min'] = rooms_min
    else:
        pass
    rooms_max = False
    if 'rooms_max' in request.GET:
        rooms_max = request.GET.get('rooms_max', False)
    if rooms_max or 'rooms_max' in request.session:
        request.session['rooms_max'] = rooms_max
        context['rooms_max'] = rooms_max

    # is_furnished
    request.session['furnished'] = False
    if 'furnished' in request.GET:
        furnished = request.GET.get('furnished', False)
        request.session['furnished'] = furnished
    else:
        if 'furnished' in request.session:
            request.session['furnished'] = furnished

    furnished = i(furnished) if furnished else False

    # check order queryset params
    if 'order_field' in request.GET:
        order_field = request.GET.get('order_field', False)
    if 'order_direction' in request.GET:
        order_direction = request.GET.get('order_direction', False)

    # check per page queryset limits
    if 'perpage' in request.GET:
        perpage = getPositiveIntVal(request.GET['perpage'])
        if perpage == 1:
            perpage = 30
        request.session['perpage'] = perpage

    if 'page' in request.GET:
        page = getPositiveIntVal(request.GET['page'])
        request.session['page'] = page

    query = ''
    # default case, when we have type & category & address
    if type:
        query += '@type ' + type
    if category:
        query += ' @category ' + category
    if address:
        if multiple_address:
            s = '|'.join(multiple_address).strip()
            s = normalize(s)
            addressTags = s.replace(' ', '').replace("'", '').replace("-", "")
            query += ' @(postalcode,city) ' + addressTags
        else:
            query += ' @(postalcode,city) ' + address
    """
    if type and category and address:
        if multiple_address:
            s = '|'.join(multiple_address).strip()
            s = normalize(s)
            addressTags =  s.replace(' ', '').replace("'",'').replace("-", "")
            query += '@type ' + type + ' @category ' + category + ' @(postalcode,city) ' + addressTags
        else:
            query += '@type ' + type + ' @category ' + category + ' @(postalcode,city) ' + address

    # search by category or list category objects with custom type
    elif type and category and not address:
        query += '@type ' + type + ' @category ' + category
    # search by type or list type objects with no category and no address
    elif type and not category and not address:
        query += '@type ' + type
    else:
        query = ''
    """

    # print "query:" + query
    request.session['query'] = query


    #
    # Do sphinx search
    #
    # if we don't have additional parameters
    results = Ad.search.query(query) # .filter(is_published=1)
    # modify query and add additional parameters like price, rooms and area
    # clear filter flags
    request.session['price_filter'] = False
    request.session['area_filter'] = False
    request.session['rooms_filter'] = False

    # TODO: optimize this count
    if Ad.search.query(query).count(): # here we check if were any ads without additional filters
        # TODO: need to be optimized coz trigger 6 queries
        # price
        filtersInitial['price_min'] = Ad.search.query(query).order_by('price')[0].price or 0
        filtersInitial['price_max'] = Ad.search.query(query).order_by('-price')[0].price or 0
        # area
        filtersInitial['area_min'] = Ad.search.query(query).order_by('area')[0].area or 0
        filtersInitial['area_max'] = Ad.search.query(query).order_by('-area')[0].area or 0
        # rooms
        filtersInitial['rooms_min'] = Ad.search.query(query).order_by('rooms')[0].rooms or 0
        filtersInitial['rooms_max'] = Ad.search.query(query).order_by('-rooms')[0].rooms or 0
        request.session['filtersInitial'] = filtersInitial

    '''
    page_perpage = False
    page_perpage = getPerageIntVal(page)
    if 'page_perpage' in request.GET:
        page_perpage = request.GET.get('page_perpage', False)
    if 'page_perpage' in request.session:
        request.session['page'] = getPerageIntVal(page)

    page_page = False
    page_page = getPageIntVal(page)
    if 'page_page' in request.GET:
        page_page = request.GET.get('page_page', False)
    if 'page_page' in request.session:
        request.session['page_page'] = getPageIntVal(page)
    context['page_page'] = page_page
    context['page_perpage'] = page_perpage
    page['page'] = page_page
    page['perpage'] = page_perpage
    '''


    # filter by price
    if price_min or price_max:
        request.session['price_filter'] = True
        # [1..2]
        if price_min and price_max:
            results = results.filter(price__gte=price_min).filter(price__lte=price_max)
            # [1 .. x]
        elif price_min and not price_max:
            results = results.filter(price__gte=price_min)
            # [x .. 2]
        elif price_max and not price_min:
            results = results.filter(price__lte=price_max)
    # filter by area
    if area_min or area_max:
        request.session['area_filter'] = True
        # [1..2]
        if area_min and area_max:
            results = results.filter(area__gte=area_min).filter(area__lte=area_max)
            # [1 .. x]
        elif area_min and not area_max:
            results = results.filter(area__gte=area_min)
            # [x .. 2]
        elif area_max and not area_min:
            results = results.filter(area__lte=area_max)
    # filter by rooms
    if rooms_min or rooms_max:
        request.session['rooms_filter'] = True
        # [1..2]
        if rooms_min and rooms_max:
            results = results.filter(rooms__gte=float(rooms_min)).filter(rooms__lte=float(rooms_max))
            # [1 .. x]
        elif rooms_min and not rooms_max:
            results = results.filter(rooms__gte=float(rooms_min))
            # [x .. 2]
        elif rooms_max and not rooms_min:
            results = results.filter(rooms__lte=float(rooms_max))
    # is furnished
    if furnished:
        results = results.filter(is_furnished=furnished)
    # order filters
    if order_field:
        if order_field == 'date':
            if order_direction == 'desc':
                results = results.order_by('-date_created')
            else:
                results = results.order_by('date_created')
        elif order_field == 'price':
            if order_direction == 'desc':
                results = results.order_by('-price')
            else:
                results = results.order_by('price')
        elif order_field == 'rooms':
            if order_direction == 'desc':
                results = results.order_by('-rooms')
            else:
                results = results.order_by('rooms')
        elif order_field == 'area':
            if order_direction == 'desc':
                results = results.order_by('-area')
            else:
                results = results.order_by('area')
        else:
            results = results.order_by('date_created')


    # ? or &
    have_filters = request.session.get('price_filter', False) or request.session.get('area_filter', False) or request.session.get('rooms_filter', False)
    # write search history in session
    # request.session['search_history'] = []
    #request.session['search_history_query_list'] = []
    if 'search_history_query_list' not in request.session:
        request.session['search_history_query_list'] = []
    if 'search_history' not in request.session:
        request.session['search_history'] = []
    search_history_query_list = request.session.get('search_history_query_list', False)
    search_history = request.session.get('search_history', False)
    if query and query not in search_history_query_list:
        d = {"query": query, "type": type, "category": category, "address": address, "url": request.build_absolute_uri()}
        search_history.append(d)
        search_history_query_list.append(query)

    # define page title
    titleType = 'Rent' if type.lower() == 'louer' else 'Buy'
    titleAddress = address.title() if address else 'VD'
    context['title'] = '%s for %s a %s' % (category.title(), titleType, titleAddress)

    resultsCount = results.count() # found ads count with additional filters

    # create tags var
    address_tags = {
        'class': 'address',
        'value': multiple_address if multiple_address else address
    }
    price_tags = {
        'class':'price',
        'from': price_min,
        'to': price_max,
        }
    area_tags = {
        'class':'area',
        'from': area_min,
        'to': area_max,
        }
    rooms_tags = {
        'class':'rooms',
        'from': rooms_min,
        'to': rooms_max,
        }
    # create huge dictionary
    tags = {
        'address': address_tags,
        'furnished': True if furnished else False,
        'price': price_tags if request.session.get('price_filter', False) else False,
        'area': area_tags if request.session.get('area_filter', False) else False,
        'rooms': rooms_tags if request.session.get('rooms_filter', False) else False,
        }

    context["page_url"] = request.build_absolute_uri()
    request.session["search_page_url"] = context["page_url"]

    '''
    context['page_page'] = page_page
    context['page_perpage'] = page_perpage
    context['page_perpage'] = page_perpage
    page['page'] = page_page
    page['perpage'] = page_perpage
    '''


    # create for class object and populate it
    formDict = {
        'type': type,
        'category': category,
        'address': address,
        # additional params
        'price_min': price_min,
        'price_max': price_max,
        'area_min': area_min,
        'area_max': area_max,
        'rooms_min': rooms_min,
        'rooms_max': rooms_max,
        'furnished': furnished,
        # order
        'order_field': order_field,
        'order_direction': order_direction,
        # perpage
        'perpage': perpage,
        'page': page,
    }
    #request.session.flush()
    request.session['formDict'] = formDict
    # params dict
    price = {}
    area = {}
    rooms = {}
    city = ''

    city = city if city else address
    price['min'] = price_min
    price['max'] = price_max
    area['min'] = area_min
    area['max'] = area_max
    rooms['min'] = rooms_min
    rooms['max'] = rooms_max
    multipleCategory = category
    categoryTags = ''
    categoryTags = category.split('|') if '|' in category else category.split(', ')
    addressTags = ''
    addressTags = address.split('|') if '|' in address else address.split(', ')
    chpu_url = ''

    query_dict = {}

    # category
    if category:
        query_dict["category"] = category
        if categoryTags.__len__()>1:
            arr = '-et-'.join(categoryTags)
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + arr
        else:
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-%s-' % category
    # type
    if type:
        query_dict["type"] = type
        chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-a-%s-' % type
    # address
    if address:
        query_dict["address"] = address
        aTags = ''
        if isinstance(addressTags, list):
            aTags = addressTags
            aTags = [item.strip() for item in aTags]
        if "|" in addressTags:
            aTags = addressTags.split('|')
            aTags = [item.strip() for item in aTags]
        if "," in addressTags:
            aTags = addressTags.split(',')
            aTags = [item.strip() for item in aTags]
        if aTags.__len__()>1:
            for item in aTags:
                chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-%s-' % item
        else:
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-%s-' % address
    # price
    if price_min or price_max:
        if price_min:
            query_dict["price_min"] = price_min
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-prix-de-%s-' % price_min
        if price_max:
            query_dict["price_max"] = price_max
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-prix-a-%s-' % price_max
    # area
    if area_min or area_max:
        if area_min:
            query_dict["area_min"] = area_min
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-area-de-%s-' % area_min
        if area_max:
            query_dict["area_max"] = area_max
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-area-a-%s-' % area_max
    # rooms
    if rooms_min or rooms_max:
        if rooms_min:
            query_dict["rooms_min"] = rooms_min
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-pieces-de-%s-' % rooms_min
        if rooms_max:
            query_dict["rooms_max"] = rooms_max
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-pieces-a-%s-' % rooms_max
    # order
    if order_field or order_direction:
        if order_field:
            query_dict["order_field"] = order_field
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-order-by-%s-' % order_field
        if order_direction:
            query_dict["order_direction"] = order_direction
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-order-direction-%s-' % order_direction
    # page
    if page or perpage:
        if page:
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-page-%s-' % page
        if perpage:
            query_dict["perpage"] = perpage
            chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-perpage-%s' % perpage

    # furnished
    if furnished:
        query_dict["furnished"] = furnished
        chpu_url = removeLeadOrTrailingSeparator(chpu_url) + '-meuble'

    context['chpu_url'] = chpu_url
    context['addressTitle'] = addressTitle
    context['categoryTitle'] = category.title()

    #remove default values for more SEO
    if "type" in query_dict and query_dict["type"] == 'louer':
        del query_dict["type"]
    if query_dict["order_field"] == 'date':
        del query_dict["order_field"]
    if query_dict["order_direction"] == 'desc':
        del query_dict["order_direction"]
    if query_dict["perpage"] == 30:
        del query_dict["perpage"]

    # remove empty/False
    for f, v in query_dict.items():
        if not v or v == u'0':
            del query_dict[f]

    context['query_str'] = '&'.join([f + "=" + str(v) for f, v in query_dict.items()])

    # remove empty/False values to form be correct
    for f, v in formDict.items():
        if not v or v == u'0':
            del formDict[f]

    request.session['chpu_url'] = chpu_url
    form = SearchFormLouer(formDict)
    if form.is_valid():
        #form.type._initial = type
        context['form'] = form
        request.session['search_history'] = search_history[-5:]
        request.session['search_history_query_list'] = search_history_query_list
        request.session['last_search_url'] = request.build_absolute_uri()
        # build context
        context['filtersInitial'] = filtersInitial
        context["paginator"] = Paginator(results, perpage)
        context["results_count"] = resultsCount
        context["type"] = type
        context["category"] = category
        context["address"] = address
        context["tags"] = tags
        context["query"] = query
        #pg = getPageIntVal(page) if getPageIntVal(page) and getPageIntVal(page) > 0 else 1
        #request.session['page_value'] = getPageIntVal(page)
        pg = page
        try:
            context["object_list"] = context["paginator"].page(pg)
        except EmptyPage as e:
            request.session['page_value'] = pg
            context["object_list"] = context["paginator"].page(1)
        #    context["object_list"] = context["paginator"].page(1)

        # get paginator list range
        debug = ''
        limit = 5
        #page = i(page)
        pagelist = context['paginator'].page_range
        maxPage = m(pagelist[-1:])
        if page == pagelist[0]:
            pagelist = pagelist[:limit]
        elif page == maxPage:
            pagelist = pagelist[-limit:]
        else:
            if context["object_list"].has_previous():
                leftpos = pg-3 if pg-3 > 0 else 0
                rightpos = limit+pg-3 if pg+2 < maxPage else maxPage
                if not leftpos:
                    rightpos += 1
                if rightpos == maxPage and not pg+2 == maxPage:
                    leftpos -= 1
                    #pass
                if leftpos == -1:
                    pagelist = pagelist[1:rightpos]
                else:
                    pagelist = pagelist[leftpos:rightpos]
                debug = "l %s, r %s, %s, limit+pg-3 %s" % (leftpos, rightpos, pg+2, limit+pg-3)
            else:
                if context["object_list"].has_next():
                    leftpos = pg+3 if pg+3 > 0 else 0
                    rightpos = limit+pg+3 if limit+pg+3 < pagelist[-1:] else pagelist[-1:]
                    pagelist = pagelist = pagelist[leftpos:rightpos]
        context["pagelist"] = pagelist
        context['maxpage'] = i(request.GET.get('page', False))
        context["page"] = page #if page <= i(maxPage) else 1
        context["search_history"] = request.session.get('search_history', False)
        context["have_filters"] = have_filters
        context["var_prefix"] = '&' if have_filters else '?'
        context['order_field'] = order_field
        context['order_direction'] = order_direction
        context['perpage'] = perpage
        context['furnished'] = furnished

        #return HttpResponseRedirect('/%s' % removeLeadOrTrailingSeparator(chpu_url)) # return result without any filter
        #return searchByParam(request, queryParam = query, categoryParam=category, typeParam=type, cityParam=city, addressParam=address, priceParam=price, roomsParam=rooms, areaParam=area, furnishedParam=furnished, multipleCategoryParam=multipleCategory)
        return render_to_response('front/ad_search.html', context, context_instance=RequestContext(request))
    else:
        # print form.errors

        form = SearchFormLouer()
        context['form'] = form
        request.session['search_history'] = search_history[-5:]
        request.session['search_history_query_list'] = search_history_query_list
        # build context
        context['filtersInitial'] = filtersInitial
        context["paginator"] = Paginator(results, page)
        context["results_count"] = resultsCount
        context["type"] = type
        context["category"] = category
        context["address"] = address
        context["tags"] = tags
        context["query"] = query
        # pg = getPageIntVal(page) if getPageIntVal(page) and getPageIntVal(page) > 0 else 1
        pg = page
        try:
            context["object_list"] = context["paginator"].page(pg)
        except EmptyPage as e:
            context["object_list"] = context["paginator"].page(1)
        # get paginator list range
        limit = 5
        #page = i(page)
        pagelist = context['paginator'].page_range
        maxPage = m(pagelist[-1:])
        if pg == pagelist[0]:
            pagelist = pagelist[:limit]
        elif pg == maxPage:
            pagelist = pagelist[-limit:]
        else:
            if context["object_list"].has_previous():
                leftpos = pg-3 if pg-3 > 0 else 0
                rightpos = limit+pg-3 if pg+2 < maxPage else maxPage
                if not leftpos:
                    rightpos += 1
                if rightpos == maxPage and not pg+2 == maxPage:
                    leftpos -= 1
                    #pass
                pagelist = pagelist = pagelist[leftpos:rightpos]
                debug = "l %s, r %s, %s, limit+pg-3 %s" % (leftpos, rightpos, pg+2, limit+pg-3)
            else:
                if context["object_list"].has_next():
                    leftpos = pg+3 if pg+3 > 0 else 0
                    rightpos = limit+pg+3 if limit+pg+3 < pagelist[-1:] else pagelist[-1:]
                    pagelist = pagelist = pagelist[leftpos:rightpos]

        context["pagelist"] = pagelist
        context["page"] = pg if pg <= maxPage else 1
        context["search_history"] = request.session.get('search_history', False)
        context["have_filters"] = have_filters
        context['order_field'] = order_field
        context['order_direction'] = order_direction
        context['perpage'] = perpage
        context['furnished'] = furnished
        canonicalLink = ''
        if category or type or address:#(furnished or price_min or price_max or area_min or area_max or rooms_min or rooms_max):
            if category:
                canonicalLink = canonicalLink + '%s-' % category
            if type:
                canonicalLink = canonicalLink + '%s-' % type
            if address:
                canonicalLink = canonicalLink + '%s-' % address
        request.session['canonicalLink'] = canonicalLink
        context['canonicalLink'] = canonicalLink

        #return HttpResponseRedirect('/%s' % removeLeadOrTrailingSeparator(chpu_url)) # return result without any filter
        #return searchByParam(request, queryParam = query, categoryParam=category, typeParam=type, cityParam=city, addressParam=address, priceParam=price, roomsParam=rooms, areaParam=area, furnishedParam=furnished, multipleCategoryParam=multipleCategory)
        return render_to_response('front/ad_search.html', context, context_instance=RequestContext(request))

def last_visitedItemRemove(request, id=''):
    #request.session.flush()
    itemList = request.session.get('last_visited', False)
    if itemList:
        if id in itemList:
            try:
                itemList.remove(id)
                request.session['last_visited'] = itemList
                return HttpResponse('Item %s successfully removed!' % id)
            except ValueError:
                return HttpResponse('Nothing to remove! itemList is empty!')
        elif id == '000':
            request.session['last_visited'] = []
            return HttpResponse('itemList successfully flushed!')
        else:
            return HttpResponse('Item %s not in %s' % (id, itemList))
    else:
        return HttpResponse('Nothing to remove! itemList is empty!')

# main chpu function
def chpu(request, query=''):
    def getValue(str='', query=query):
        a = ''
        if str:
            if query.find(str):
                a = query[query.find(str):].replace(str,'').split('-')[0]
        return a

    def getValueFromRight(str='', query=query):
        a = ''
        if str in query:
            if query.find(str):
                a = query[query.find(str):].replace(str,'').split('-')
                a = filter(None,a)[0]
            else:
                return ''
        return a

    def getValueFromLeft(str='', query=query):
        a = ''
        if str:
            if query.find(str):
                a = query[-query.find(str):].split('-')
        return a.reverse()

    def look(needle='', haystack=''):
        if needle and haystack:
            if needle in haystack:
                return True
            else:
                return False

    if query and len(query)>1:
        query = query.lower()
        if ',' in query:
            query = query.replace(',', '-')
        if '|' in query:
            query = query.replace('|', '-')

        request.session['query-debug'] = query
        chpuDict = {
            "categoryAndType" : {u'appartement-a-louer', u'maison-a-louer', u'studio-a-louer', u'chambre-a-louer', u'colocation-a-louer', u'appartement-a-vendre', u'maison-a-vendre', u'studio-a-vendre', u'appartement-a-archeter', u'maison-a-archeter', u'studio-a-archeter'}, "categoryOrType" : {u'studio', u'appartement', u'maison', u'chambre', u'colocation', u'acheter', u'louer', 'vendre'},
            'type':{u'acheter', u'louer', 'vendre'},
            'category':{u'appartement', u'maison', u'studio', u'colocation'},
            "rooms" : {u'pieces-de', u'pieces-a', u'piece-de', u'piece-a'},
            'price': {u'prix-de', u'prix-a', u'price-from', u'price-to'},
            'area': {u'surface-hebitable-de', u'surface-hebitable-a', u'area-de', u'area-a'},
            'furnished':{u'meuble', u'furnished'}, 'addressDict':{'lausanne','grandson','gverdon','echallens','groye-gully','cossonay','orbe', 'payerne','lavaux', 'oron','vevey-montreux', "pays-d'enhaut", "pays-d-enhaut", "pays-enhaut", 'morges', 'la-vallee', 'nyon','aubonne', 'rolle', 'aigle'},
            'furnishedDict':{'furnished', 'immeuble', 'meuble'},
            'multipleCategory':{u'studio-et-appartement', u'studio-et-maison', u'studio-et-chambre', u'studio-et-colocation',
                                u'appartement-et-studio', u'appartement-et-maison', u'appartement-et-chambre', u'appartement-et-colocation',
                                u'maison-et-studio', u'maison-et-appartement', u'maison-et-chambre', u'maison-et-colocation',
                                u'chambre-et-studio', u'chambre-et-appartement', u'chambre-et-maison', u'maison-et-colocation',
                                u'colocation-et-studio', u'colocation-et-appartement', u'colocation-et-maison' },
            'order':{u'order-by', u'order-direction'},
            'page':{u'page', u'perpage'},
}

        chpuSearchParams = {}
        chpuParams = {}
        price = {}
        rooms = {}
        area = {}
        order = {}
        page = {}
        opions = {}
        typeAndCategoryMode = False
        multipleCategory = False
        category = ''
        type= ''
        furnished = ''
        address = ''
        city = ''

        # check for type
        for keyword in chpuDict['type']:
            if keyword in query:
                if keyword == 'louer':
                    type = "louer"
                if keyword == "acheter":
                    type = "acheter"
                if keyword == "vendre":
                    type = "acheter"

        # Multiple category
        for keyword in chpuDict['multipleCategory']:
            if keyword in query:
                multipleCategory = True
                separator = '|'
                request.session['MultiplecategoryFoundData'] = "%s|||||%s" % (keyword, query)
                if keyword in query:
                    request.session['categoryFound'] = multipleCategory
                    kword = keyword
                    kword = str(kword)
                    kword = kword.replace('-et-', separator).strip()
                    category = sorted(kword.split("|"))
                    category = "|".join(category)
                    multipleCategory = category

        # Single category mode
        if not multipleCategory:
            for keyword in chpuDict['category']:
                if keyword in query:
                    request.session['SinglecategoryFoundData'] = "%s|||||%s" % (keyword, query)
                    for keyword in chpuDict['categoryOrType']:
                        if keyword in query:
                            # category
                            if keyword == 'appartement':
                                category = 'appartement'
                            if keyword == 'maison':
                                category = 'maison'
                            if keyword == 'studio':
                                category = 'studio'
                            if keyword == 'colocation':
                                category = 'colocation'
                            if keyword == 'chambre':
                                category = 'colocation'

        # address
        for keyword in chpuDict['addressDict']:
            separator = ', '
            if keyword.lower() in query:
                #address = address+''+keyword.lower()
                if address.__len__():
                    address = keyword.lower()+separator+address
                else:
                    address = keyword.lower()
                address = sorted(address.split(', '))
                address = ", ".join(address)

        # rooms
        for keyword in chpuDict['rooms']:
            if keyword in query:
                if 'pieces-de-' in query:
                    rooms['min'] = getValueFromRight('pieces-de-')
                if 'pieces-a-' in query:
                    rooms['max'] = getValueFromRight('pieces-a-')
                if 'piece-de-' in query:
                    rooms['min'] = getValueFromRight('piece-de-')
                if 'piece-a-' in query:
                    rooms['max'] = getValueFromRight('piece-a-')
                if 'rooms-de-' in query:
                    rooms['min'] = getValueFromRight('rooms-de-')
                if 'rooms-a-' in query:
                    rooms['max'] = getValueFromRight('rooms-a-')
        # area
        for keyword in chpuDict['area']:
            if keyword in query:
                if 'surface-hebitable-de-' in query:
                    area['min'] = getValueFromRight('surface-hebitable-de-')
                if 'surface-hebitable-a-' in query:
                    area['max'] = getValueFromRight('surface-hebitable-a-')
                if 'surface-hebitable-de-' in query:
                    area['min'] = getValueFromRight('surface-hebitable-de-')
                if 'surface-hebitable-a-' in query:
                    area['max'] = getValueFromRight('surface-hebitable-a-')
                if 'area-de-' in query:
                    area['min'] = getValueFromRight('area-de-')
                if 'area-a-' in query:
                    area['max'] = getValueFromRight('area-a-')
        # price
        for keyword in chpuDict['price']:
            if keyword in query:
                request.session['chat'] = price
                if keyword == 'prix-de':
                    price['min'] = getValueFromRight('prix-de-')
                if keyword == 'prix-a':
                    price['max'] = getValueFromRight('prix-a-')
                if keyword == 'price-from':
                    price['min'] = getValueFromRight('price-from-')
                if keyword == 'price-to':
                    price['max'] = getValueFromRight('price-to')

        # furnished
        for keyword in chpuDict['furnishedDict']:
            if keyword in query:
                furnished = 1
        # order
        for keyword in chpuDict['order']:
            if keyword in query:
                if 'order-by-' in query:
                    order['order_field'] = getValueFromRight('order-by-')
                if 'order-direction-' in query:
                    request.session['debug-url'] = getValueFromRight('order-by-')
                    order['order_direction'] = getValueFromRight('order-direction-')
        # page
        for keyword in chpuDict['page']:
            if keyword in query:
                if 'page-' in query:
                    page['page'] = getValueFromRight('page-')
                if 'perpage' in query:
                    page['perpage'] = getValueFromRight('perpage-')
        # debug
        request.session['aDEBUG-'] = [type, category,address, price, rooms, area, furnished, order, page, opions, multipleCategory]

        return searchByParam(request, queryParam = query, categoryParam=category, typeParam=type, cityParam=city, addressParam=address, priceParam=price, roomsParam=rooms, areaParam=area, furnishedParam=furnished, orderParam=order, pageParam=page, optionsParam=opions, multipleCategoryParam=multipleCategory)


CITIES = (
    # city_slug, city_name
    ('aigle', 'aigle'),
    ('broye-vully', 'broye-vully'),
    ('cossonay', 'cossonay'),
    ('echallens', 'echallens'),
    ('grandson', 'grandson'),
    ('aubonne', 'aubonne'),
    ('lausanne', 'lausanne'),
    ('lavaux', 'lavaux'),
    ('montreux', 'montreux'),
    ('morges', 'morges'),
    ('nyon', 'nyon'),
    ('orbe', 'orbe'),
    ('oron', 'oron'),
    ('payerne', 'payerne'),
    ('rolle', 'rolle'),
    ('vevey', 'vevey'),
    ('yverdon', 'yverdon'),
)

ROOMS = (
    # rooms_min, rooms_max
    ('2', '2.5'),
    ('3', '3.5'),
    ('4', '4.5'),
    ('5', '5.5'),
    ('6', '6.5'),
)

def sitemap(request):
    context = {}
    context['TYPE_OPTIONS'] = TYPE_OPTIONS

    return render(request, 'sitemap.xml', context)


def sitemap_type(request, type_code):
    context = {}
    context['type_code'] = type_code
    categoryies = [x.lower() for x, y in CATEGORY_OPTIONS]

    if type_code == 'acheter' and 'colocation' in categoryies:
        categoryies.remove('colocation')

    context['CATEGORIES'] = categoryies
    context['CITIES'] = CITIES

    return render(request, 'sitemap_type.xml', context)


def sitemap_category(request, type_code, cat_code):
    context = {}
    context['type_code'] = type_code
    context['cat_code'] = cat_code
    context['CITIES'] = CITIES

    return render(request, 'sitemap_category.xml', context)


def sitemap_city(request, type_code, cat_code, city_slug):
    context = {}
    context['type_code'] = type_code
    context['cat_code'] = cat_code
    context['city_slug'] = city_slug
    context['ROOMS'] = ROOMS if cat_code == 'appartement' else []

    return render(request, 'sitemap_city.xml', context)



def sitemapPage(request):
    context = {}
    context['cityListPreset'] = ['Aigle', 'Aubonne', 'Broye-Vully', 'Cossonay',
        'Echallens', 'Grandson', 'La Vallee', 'Lausanne',
        'Lavaux', 'Montreux', 'Morges', 'Nyon', 'Orbe', 'Oron',
        'Payerne', "Pays d'Enhaut", 'Rolle', 'Vevey', 'Yverdon']

    return render_to_response('front/sitemap.html', context, context_instance=RequestContext(request))



def redirect500(request):
    return redirect(indexPage)

def redirect400(request):
    return redirect(indexPage)

def redirect403(request):
    return redirect(indexPage)


def debugView(request, param='debug'):
    return HttpResponse(param)
