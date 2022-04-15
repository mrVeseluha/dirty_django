from frame_core.view import BaseView
from .models import *

logger = ViewLogger()
model_logger = ModelLogger()
CATEGORIES = []
COURSES = []

class HomeView(BaseView):
    template = 'courses/index.html'
    
    def __init__(self, *args, **kwargs):
        logger.log('Вызвана функция рендеринга главной страницы')
        return super(HomeView, self).__init__(*args, **kwargs)

    def get_context(self):
        context = super(HomeView, self).get_context()
        context['courses'] = COURSES
        context['categories'] = CATEGORIES
        return context
    
    def GET(self):
        clone_id = self.request.get('GET')
        if clone_id:
            clone_id = int(clone_id.get('clone'))
            clone = COURSES[clone_id].clone()
            clone.name += ' (копия)'
            COURSES.append(clone)
            model_logger.log(f'Создана копия курса: {COURSES[-1]}')
        return super(HomeView, self).GET()
    
    def POST(self):
        print(self.request.get('POST'))
        new_course = Course(**self.request.get('POST'))
        if 'category' in self.request['POST']:
            if new_course.category == '':
                new_course.category = None
            else:
                new_course.category = CATEGORIES[int(new_course.category)].name
        COURSES.append(new_course)
        model_logger.log(f'Создана новый курс: {COURSES[-1]}')
        return super(HomeView, self).POST()


class CategoriesView(BaseView):
    template = 'courses/categories.html'

    def get_context(self):
        logger.log('Вызвана функция рендеринга категорий курсов')
        context = super(CategoriesView, self).get_context()
        context['categories'] = CATEGORIES
        return context
    
    def GET(self):
        clone_id = self.request.get('GET')
        if clone_id:
            clone_id = int(clone_id.get('clone'))
            clone = CATEGORIES[clone_id].clone()
            clone.name += ' (копия)'
            CATEGORIES.append(clone)
            model_logger.log(f'Создана копия категории: {CATEGORIES[-1]}')
        return super(CategoriesView, self).GET()

    def POST(self):
        CATEGORIES.append(CourseCategory(**self.request.get('POST')))
        model_logger.log(f'Создана новая категория: {CATEGORIES[-1]}')
        return super(CategoriesView, self).POST()
