from django.test import TestCase

from goals.models import Goal
from tasks.models import Task
from tasks.tests.helpers import setup_tasks
from tasks import exceptions as tasks_exceptions


class TestStatusTransitions(TestCase):
    # def test_transition_to_completed_with_no_subtask(self):
    #     Goal.objects.create(id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472')
    #     (
    #         task_first,
    #         task_second,
    #         task_third,
    #     ) = setup_tasks(
    #         f"""id,parent_id,text,status
    #         6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-0,not_started
    #         129e70c2-ff7b-4130-9117-f9bc035246e0,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-1,in_progress
    #         033f3ae4-659d-47ff-a53b-e2579a9a643c,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-3,completed
    #         """
    #     )

    #     task_first.transition_to('completed')
    #     task_second.transition_to('completed')
    #     task_third.transition_to('completed')

    #     task_first.refresh_from_db()
    #     task_second.refresh_from_db()
    #     task_third.refresh_from_db()
    #     self.assertEqual(task_first.status, 'completed')
    #     self.assertEqual(task_second.status, 'completed')
    #     self.assertEqual(task_third.status, 'completed')

    # def test_transition_to_in_progress_with_no_subtask(self):
    #     Goal.objects.create(id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472')
    #     (
    #         task_first,
    #         task_second,
    #         task_third,
    #     ) = setup_tasks(
    #         f"""id,parent_id,text,status
    #         6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-0,not_started
    #         129e70c2-ff7b-4130-9117-f9bc035246e0,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-1,in_progress
    #         033f3ae4-659d-47ff-a53b-e2579a9a643c,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-3,completed
    #         """
    #     )

    #     task_first.transition_to('in_progress')
    #     task_second.transition_to('in_progress')
    #     task_third.transition_to('in_progress')

    #     task_first.refresh_from_db()
    #     task_second.refresh_from_db()
    #     task_third.refresh_from_db()
    #     self.assertEqual(task_first.status, 'in_progress')
    #     self.assertEqual(task_second.status, 'in_progress')
    #     self.assertEqual(task_third.status, 'in_progress')

    # def test_transition_to_completed_with_subtasks(self):
    #     Goal.objects.create(id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472')
    #     (
    #         task_first,
    #         task_first_subtask_first,
    #         task_first_subtask_second,
    #         task_second,
    #         task_second_subtask_first,
    #         task_second_subtask_second,
    #         task_third,
    #         task_third_subtask_first,
    #         task_third_subtask_second,
    #     ) = setup_tasks(
    #         f"""id,parent_id,text,status
    #         6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-0,not_started
    #         9aaab701-2681-4f9c-a4d3-c08dbc5f7c22,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-1,not_started
    #         4d5d5d05-3396-45aa-8238-a7ec6e62bac0,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-2,not_started
    #         0696d065-e8c1-44d7-b7aa-ffd6ec67ed2f,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-3,in_progress
    #         5d9de343-5b90-4b2a-a226-cbd1848b1e41,0696d065-e8c1-44d7-b7aa-ffd6ec67ed2f,some-text-4,in_progress
    #         1f7ee8bb-1348-4e81-b986-d2dbd2c311f8,0696d065-e8c1-44d7-b7aa-ffd6ec67ed2f,some-text-5,not_started
    #         21f0d4eb-1799-4937-99f4-be66093a3b9b,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-6,completed
    #         129e70c2-ff7b-4130-9117-f9bc035246e0,21f0d4eb-1799-4937-99f4-be66093a3b9b,some-text-7,completed
    #         033f3ae4-659d-47ff-a53b-e2579a9a643c,21f0d4eb-1799-4937-99f4-be66093a3b9b,some-text-8,completed
    #         """
    #     )

    #     task_first.transition_to('completed')
    #     task_second.transition_to('completed')
    #     task_third.transition_to('completed')

    #     task_first.refresh_from_db()
    #     task_first_subtask_first.refresh_from_db()
    #     task_first_subtask_second.refresh_from_db()
    #     task_second.refresh_from_db()
    #     task_second_subtask_first.refresh_from_db()
    #     task_second_subtask_second.refresh_from_db()
    #     task_third.refresh_from_db()
    #     task_third_subtask_first.refresh_from_db()
    #     task_third_subtask_second.refresh_from_db()
    #     self.assertEqual(task_first.status, 'completed')
    #     self.assertEqual(task_first_subtask_first.status, 'completed')
    #     self.assertEqual(task_first_subtask_second.status, 'completed')
    #     self.assertEqual(task_second.status, 'completed')
    #     self.assertEqual(task_second_subtask_first.status, 'completed')
    #     self.assertEqual(task_second_subtask_second.status, 'completed')
    #     self.assertEqual(task_third.status, 'completed')
    #     self.assertEqual(task_third_subtask_first.status, 'completed')
    #     self.assertEqual(task_third_subtask_second.status, 'completed')

    # def test_transition_to_completed_single_task_ancestor_single_sibling(self):
    #     Goal.objects.create(id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472')
    #     (
    #         task_first,
    #         task_first_subtask,
    #         task_second,
    #         task_second_subtask,
    #         task_third,
    #         task_third_subtask,
    #     ) = setup_tasks(
    #         f"""id,parent_id,text,status
    #         6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-0,not_started
    #         129e70c2-ff7b-4130-9117-f9bc035246e0,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-1,not_started
    #         70af52be-8d07-4bbb-adf6-f48e3537397f,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-2,in_progress
    #         c413169f-5b86-45af-b8ae-3644a3a70165,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-3,in_progress
    #         7ee65fd4-0efc-4eb5-a62b-bdb6916875f1,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-4,completed
    #         6f0acdc9-e888-4b1b-afa7-6333f01550cf,7ee65fd4-0efc-4eb5-a62b-bdb6916875f1,some-text-5,completed
    #         """
    #     )

    #     task_first_subtask.transition_to('completed')
    #     task_second_subtask.transition_to('completed')
    #     task_third_subtask.transition_to('completed')

    #     task_first.refresh_from_db()
    #     task_first_subtask.refresh_from_db()
    #     task_second.refresh_from_db()
    #     task_second_subtask.refresh_from_db()
    #     task_third.refresh_from_db()
    #     task_third_subtask.refresh_from_db()

    #     self.assertEqual(task_first.status, 'completed')
    #     self.assertEqual(task_first_subtask.status, 'completed')
    #     self.assertEqual(task_second.status, 'completed')
    #     self.assertEqual(task_second_subtask.status, 'completed')
    #     self.assertEqual(task_third.status, 'completed')
    #     self.assertEqual(task_third_subtask.status, 'completed')

    # def test_transition_to_completed_with_descendant_subtasks(self):
    #     Goal.objects.create(id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472')
    #     (
    #         task,
    #         subtask,
    #         subsubtask_first,
    #         subsubtask_second,
    #     ) = setup_tasks(
    #         f"""id,parent_id,text,status
    #         6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-0,in_progress
    #         129e70c2-ff7b-4130-9117-f9bc035246e0,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-1,in_progress
    #         033f3ae4-659d-47ff-a53b-e2579a9a643c,129e70c2-ff7b-4130-9117-f9bc035246e0,some-text-2,not_started
    #         ef4fa073-ce1a-469c-a206-91b04d83006b,129e70c2-ff7b-4130-9117-f9bc035246e0,some-text-3,in_progress
    #         """
    #     )

    #     task.transition_to('completed')

    #     task.refresh_from_db()
    #     subtask.refresh_from_db()
    #     subsubtask_first.refresh_from_db()
    #     subsubtask_second.refresh_from_db()
    #     self.assertEqual(task.status, 'completed')
    #     self.assertEqual(subtask.status, 'completed')
    #     self.assertEqual(subsubtask_first.status, 'completed')
    #     self.assertEqual(subsubtask_second.status, 'completed')

    # def test_transition_to_in_progress_with_subtasks(self):
    #     Goal.objects.create(id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472')
    #     (
    #         task,
    #         subtask_first,
    #         subtask_second,
    #     ) = setup_tasks(
    #         f"""id,parent_id,text,status
    #         6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-0,not_started
    #         129e70c2-ff7b-4130-9117-f9bc035246e0,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-1,not_started
    #         033f3ae4-659d-47ff-a53b-e2579a9a643c,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-2,not_started
    #         """
    #     )

    #     task.transition_to('in_progress')

    #     task.refresh_from_db()
    #     subtask_first.refresh_from_db()
    #     subtask_second.refresh_from_db()
    #     self.assertEqual(task.status, 'in_progress')
    #     self.assertEqual(subtask_first.status, 'in_progress')
    #     self.assertEqual(subtask_second.status, 'in_progress')

    # def test_from_not_started_to_in_progress_while_all_siblings_in_progress(self):
    #     Goal.objects.create(id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472')
    #     (
    #         task_parent,
    #         task,
    #         task_sibling_first,
    #         task_sibling_second,
    #         task_sibling_third,
    #     ) = setup_tasks(
    #         f"""id,parent_id,text,status
    #         6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-0,not_started
    #         129e70c2-ff7b-4130-9117-f9bc035246e0,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-1,not_started
    #         033f3ae4-659d-47ff-a53b-e2579a9a643c,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-2,in_progress
    #         033f3ae4-659d-47ff-a53b-e2579a9a643d,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-3,in_progress
    #         033f3ae4-659d-47ff-a53b-e2579a9a643e,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-4,in_progress
    #         """
    #     )

    #     task.transition_to('in_progress')

    #     task_parent.refresh_from_db()
    #     task.refresh_from_db()
    #     self.assertEqual(task.status, 'in_progress')
    #     self.assertEqual(task_parent.status, 'in_progress')

    # def test_from_in_progress_to_completed_while_all_siblings_completed(self):
    #     Goal.objects.create(id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472')
    #     (
    #         task_parent,
    #         task,
    #         task_sibling_first,
    #         task_sibling_second,
    #         task_sibling_third,
    #     ) = setup_tasks(
    #         f"""id,parent_id,text,status
    #         6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-0,in_progress
    #         129e70c2-ff7b-4130-9117-f9bc035246e0,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-1,in_progress
    #         033f3ae4-659d-47ff-a53b-e2579a9a643c,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-2,completed
    #         033f3ae4-659d-47ff-a53b-e2579a9a643d,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-3,completed
    #         033f3ae4-659d-47ff-a53b-e2579a9a643e,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-4,completed
    #         """
    #     )

    #     task.transition_to('completed')

    #     task_parent.refresh_from_db()
    #     task.refresh_from_db()
    #     self.assertEqual(task.status, 'completed')
    #     self.assertEqual(task_parent.status, 'completed')

    # def test_from_completed_to_in_progress_while_all_siblings_in_progress(self):
    #     Goal.objects.create(id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472')
    #     (
    #         task_parent,
    #         task,
    #         task_sibling_first,
    #         task_sibling_second,
    #         task_sibling_third,
    #     ) = setup_tasks(
    #         f"""id,parent_id,text,status
    #         6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-0,completed
    #         129e70c2-ff7b-4130-9117-f9bc035246e0,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-1,completed
    #         033f3ae4-659d-47ff-a53b-e2579a9a643c,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-2,in_progress
    #         033f3ae4-659d-47ff-a53b-e2579a9a643d,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-3,in_progress
    #         033f3ae4-659d-47ff-a53b-e2579a9a643e,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-4,in_progress
    #         """
    #     )

    #     task.transition_to('in_progress')

    #     task_parent.refresh_from_db()
    #     task.refresh_from_db()
    #     self.assertEqual(task.status, 'in_progress')
    #     self.assertEqual(task_parent.status, 'in_progress')

    # def test_from_in_progress_to_not_started_while_all_siblings_not_started(self):
    #     Goal.objects.create(id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472')
    #     (
    #         task_parent,
    #         task,
    #         task_sibling_first,
    #         task_sibling_second,
    #         task_sibling_third,
    #     ) = setup_tasks(
    #         f"""id,parent_id,text,status
    #         6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-0,completed
    #         129e70c2-ff7b-4130-9117-f9bc035246e0,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-1,completed
    #         033f3ae4-659d-47ff-a53b-e2579a9a643c,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-2,in_progress
    #         033f3ae4-659d-47ff-a53b-e2579a9a643d,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-3,in_progress
    #         033f3ae4-659d-47ff-a53b-e2579a9a643e,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-4,in_progress
    #         """
    #     )

    #     task.transition_to('in_progress')

    #     task_parent.refresh_from_db()
    #     task.refresh_from_db()
    #     self.assertEqual(task.status, 'in_progress')
    #     self.assertEqual(task_parent.status, 'in_progress')

    # def test_transition_a_task_with_subtasks(self):
    #     Goal.objects.create(id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472')
    #     (
    #         task,
    #         task_subtask_first,
    #         task_subtask_second,
    #         task_substask_third,
    #     ) = setup_tasks(
    #         f"""id,parent_id,text,status
    #         6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,some-text-0,in_progress
    #         033f3ae4-659d-47ff-a53b-e2579a9a643c,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-2,in_progress
    #         033f3ae4-659d-47ff-a53b-e2579a9a643d,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-3,in_progress
    #         033f3ae4-659d-47ff-a53b-e2579a9a643e,6a844440-13a1-48fc-9974-0b0f2114eafa,some-text-4,in_progress
    #         """
    #     )

    #     with self.assertRaises(tasks_exceptions.StatusTransitionError):
    #         task.transition_to('completed')

    def test_transition_subtask_from_not_started_to_in_progress(self):
        """
        g0__not_started
        ├── t0__not_started
        └── t1__not_started
            ├── t1.1__not_started
            │   └── t1.1.1__not_started
            └── t1.2__not_started
                ├── t1.2.1__not_started
                └── t1.2.2__not_started

        Transition t1.2.1: not_started -> in_progress

        g0__not_started
        ├── t0__in_progress
        └── t1__in_progress
            ├── t1.1__in_progress
            │   └── t1.1.1__in_progress
            └── t1.2__in_progress
                ├── t1.2.1__in_progress
                └── t1.2.2__in_progress
        """
        goal = Goal.objects.create(id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472')
        (
            t0,
            t1,
            t1_1,
            t1_1_1,
            t1_2,
            t1_2_1,
            t1_2_2
        ) = setup_tasks(
            f"""id,parent_id,text,status
            6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t0,not_started
            033f3ae4-659d-47ff-a53b-e2579a9a643c,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t1,not_started
            53a6485e-3473-49bd-bc9d-2fe1d3a9707e,033f3ae4-659d-47ff-a53b-e2579a9a643c,t1.1,not_started
            f0a8399e-4941-407d-aba5-1312d16c2ed8,53a6485e-3473-49bd-bc9d-2fe1d3a9707e,t1.1.1,not_started
            c8c453d8-349f-4ac6-a061-8a16973b09b8,033f3ae4-659d-47ff-a53b-e2579a9a643c,t1.2,not_started
            a7789f7d-08f0-45e7-97b4-d091f3132d53,c8c453d8-349f-4ac6-a061-8a16973b09b8,t1.2.1,not_started
            29aa2bca-ad56-4219-8f8e-b4d73d37789d,c8c453d8-349f-4ac6-a061-8a16973b09b8,t1.2.2,not_started
            """
        )

        t1_2_1.transition_to('in_progress')

        goal.refresh_from_db()
        t0.refresh_from_db()
        t1.refresh_from_db()
        t1_1.refresh_from_db()
        t1_1_1.refresh_from_db()
        t1_2.refresh_from_db()
        t1_2_1.refresh_from_db()
        t1_2_2.refresh_from_db()
        self.assertEqual(goal.status, 'in_progress')
        self.assertEqual(t0.status, 'in_progress')
        self.assertEqual(t1.status, 'in_progress')
        self.assertEqual(t1_1.status, 'in_progress')
        self.assertEqual(t1_1_1.status, 'in_progress')
        self.assertEqual(t1_2.status, 'in_progress')
        self.assertEqual(t1_2_1.status, 'in_progress')
