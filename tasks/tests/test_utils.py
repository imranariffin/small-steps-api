from django.test import TestCase

from goals.models import Goal
from tasks import utils
from tasks.models import Task

class TestTasksUtils(TestCase):
    def test_get_parent_goal(self):
        goal_id = Goal.objects.create().id
        task = Task.objects.create(parent_id=goal_id, text='some-text-0')

        parent = utils.get_parent(task)

        self.assertEqual(parent, None)

    def test_get_siblings(self):
        goal_id = Goal.objects.create().id
        task_parent = Task.objects.create(parent_id=goal_id, text='some-text-0')
        task = Task.objects.create(parent_id=task_parent.id, text='some-text-1')
        task_sibling_first = Task.objects.create(parent_id=task_parent.id, text='some-text-2')
        task_sibling_second = Task.objects.create(parent_id=task_parent.id, text='some-text-3')

        siblings = list(utils.get_siblings(task))

        self.assertEqual(len(siblings), 2)
        self.assertEqual(siblings[0], task_sibling_second)
        self.assertEqual(siblings[1], task_sibling_first)
