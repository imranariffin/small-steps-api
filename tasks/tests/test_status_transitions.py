from django.test import TestCase

from goals.models import Goal
from tasks.tests.helpers import setup_tasks
from tasks.exceptions import InvalidStatusTransition


class TestStatusTransitions(TestCase):
    def test_transition_from_not_started_to_in_progress(self):
        """
        g0__not_started
        ├── t0__not_started
        └── t1__not_started
            ├── t1.1__not_started
            │   └── t1.1.1__not_started
            └── t1.2__not_started
                ├── t1.2.1__not_started
                └── t1.2.2__not_started
        g1__in_progress
        g2__completed

        Transition t1.2.1: not_started -> in_progress

        g0__in_progress
        ├── t0__not_started
        ├── t1__in_progress
        │   ├── t1.1__not_started
        │   │   └── t1.1.1__not_started
        │   └── t1.2__in_progress
        │       ├── t1.2.1__in_progress
        │       └── t1.2.2__not_started
        └── t2__completed
        g1__in_progress
        g2__completed
        """
        g0 = Goal.objects.create(id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472')
        g1 = Goal.objects.create(status='in_progress')
        g2 = Goal.objects.create(status='completed')
        (
            t0,
            t1,
            t1_1,
            t1_1_1,
            t1_2,
            t1_2_1,
            t1_2_2,
            t2,
        ) = setup_tasks(
            f"""id,parent_id,text,status
            6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t0,not_started
            033f3ae4-659d-47ff-a53b-e2579a9a643c,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t1,not_started
            53a6485e-3473-49bd-bc9d-2fe1d3a9707e,033f3ae4-659d-47ff-a53b-e2579a9a643c,t1.1,not_started
            f0a8399e-4941-407d-aba5-1312d16c2ed8,53a6485e-3473-49bd-bc9d-2fe1d3a9707e,t1.1.1,not_started
            c8c453d8-349f-4ac6-a061-8a16973b09b8,033f3ae4-659d-47ff-a53b-e2579a9a643c,t1.2,not_started
            a7789f7d-08f0-45e7-97b4-d091f3132d53,c8c453d8-349f-4ac6-a061-8a16973b09b8,t1.2.1,not_started
            29aa2bca-ad56-4219-8f8e-b4d73d37789d,c8c453d8-349f-4ac6-a061-8a16973b09b8,t1.2.2,not_started
            0406b08b-711e-4cc8-8698-987b4ea5a4c2,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t2,completed
            """
        )

        t1_2_1.transition_to('in_progress')

        self._refresh_from_db(
            g0, t0, t1, t1_1, t1_1_1, t1_2, t1_2_1, t1_2_2, t2, g1, g2
        )
        self.assertEqual(g0.status, 'in_progress')
        self.assertEqual(t0.status, 'not_started')
        self.assertEqual(t1.status, 'in_progress')
        self.assertEqual(t1_1.status, 'not_started')
        self.assertEqual(t1_1_1.status, 'not_started')
        self.assertEqual(t1_2.status, 'in_progress')
        self.assertEqual(t1_2_1.status, 'in_progress')
        self.assertEqual(t1_2_2.status, 'not_started')
        self.assertEqual(t2.status, 'completed')
        self.assertEqual(g1.status, 'in_progress')
        self.assertEqual(g2.status, 'completed')

    def test_transition_from_in_progress_to_completed(self):
        """
        g0__in_progress
        ├── t0__in_progress
        ├── t1__in_progress
        │   ├── t1.1__not_started
        │   │   └── t1.1.1__not_started
        │   └── t1.2__in_progress
        │       ├── t1.2.1__completed
        │       ├── t1.2.2__in_progress
        │       └── t1.2.3__not_started
        └── t2__completed
        g1__in_progress
        g2__completed

        Transition t1.2.2: in_progress -> completed

        g0__in_progress
        ├── t0__in_progress
        ├── t1__in_progress
        │   ├── t1.1__not_started
        │   │   └── t1.1.1__not_started
        │   └── t1.2__in_progress
        │       ├── t1.2.1__completed
        │       ├── t1.2.2__completed
        │       └── t1.2.3__not_started
        └── t2__completed
        g1__in_progress
        g2__completed
        """
        g0 = Goal.objects.create(
            id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472',
            status='in_progress',
        )
        g1 = Goal.objects.create(status='in_progress')
        g2 = Goal.objects.create(status='completed')
        (
            t0, t1, t1_1, t1_1_1, t1_2, t1_2_1, t1_2_2, t1_2_3, t2,
        ) = setup_tasks(
            f"""id,parent_id,text,status
            6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t0,in_progress
            033f3ae4-659d-47ff-a53b-e2579a9a643c,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t1,in_progress
            53a6485e-3473-49bd-bc9d-2fe1d3a9707e,033f3ae4-659d-47ff-a53b-e2579a9a643c,t1.1,not_started
            f0a8399e-4941-407d-aba5-1312d16c2ed8,53a6485e-3473-49bd-bc9d-2fe1d3a9707e,t1.1.1,not_started
            c8c453d8-349f-4ac6-a061-8a16973b09b8,033f3ae4-659d-47ff-a53b-e2579a9a643c,t1.2,in_progress
            a7789f7d-08f0-45e7-97b4-d091f3132d53,c8c453d8-349f-4ac6-a061-8a16973b09b8,t1.2.1,completed
            29aa2bca-ad56-4219-8f8e-b4d73d37789d,c8c453d8-349f-4ac6-a061-8a16973b09b8,t1.2.2,in_progress
            56f60eca-7821-44c2-a32e-46ff05d117f3,c8c453d8-349f-4ac6-a061-8a16973b09b8,t1.2.3,not_started
            0406b08b-711e-4cc8-8698-987b4ea5a4c2,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t2,completed
            """
        )

        t1_2_2.transition_to('completed')

        self._refresh_from_db(
            g0, t0, t1, t1_1, t1_1_1, t1_2, t1_2_1, t1_2_2, t1_2_3, t2, g1, g2,
        )
        self.assertEqual(g0.status, 'in_progress')
        self.assertEqual(t0.status, 'in_progress')
        self.assertEqual(t1.status, 'in_progress')
        self.assertEqual(t1_1.status, 'not_started')
        self.assertEqual(t1_1_1.status, 'not_started')
        self.assertEqual(t1_2.status, 'in_progress')
        self.assertEqual(t1_2_1.status, 'completed')
        self.assertEqual(t1_2_2.status, 'completed')
        self.assertEqual(t1_2_3.status, 'not_started')
        self.assertEqual(t2.status, 'completed')
        self.assertEqual(g1.status, 'in_progress')
        self.assertEqual(g2.status, 'completed')

    def test_transition_from_completed_to_in_progress(self):
        """
        g0__in_progress
        ├── t0__in_progress
        ├── t1__in_progress
        │   ├── t1.1__in_progress
        │   │   └── t1.1.1__not_started
        |   |   └── t1.1.2__completed
        │   └── t1.2__completed
        │       ├── t1.2.1__completed
        │       ├── t1.2.2__completed
        │       └── t1.2.3__completed
        └── t2__completed
            ├── t2.1__completed
            │   └── t2.1.1__completed
            └── t2.2__completed
        g1__in_progress
        g2__completed

        Transition t1.1.2: completed -> in_progress
        Transition t1.2.2: completed -> in_progress
        Transition t2.1.1: completed -> in_progress

        g0__in_progress
        ├── t0__in_progress
        ├── t1__in_progress
        │   ├── t1.1__in_progress
        │   │   ├── t1.1.1__not_started
        |   |   └── t1.1.2__in_progress
        │   └── t1.2__in_progress
        │       ├── t1.2.1__completed
        │       ├── t1.2.2__in_progress
        │       └── t1.2.3__completed
        └── t2__in_progress
            ├── t2.1__in_progress
            │   └── t2.1.1__in_progress
            └── t2.2__completed
        g1__in_progress
        g2__completed
        """
        g0 = Goal.objects.create(
            id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472',
            status='in_progress',
        )
        g1 = Goal.objects.create(status='in_progress')
        g2 = Goal.objects.create(status='completed')
        (
            t0, t1, t1_1, t1_1_1, t1_1_2, t1_2, t1_2_1,
            t1_2_2, t1_2_3, t2, t2_1, t2_1_1, t2_2,
        ) = setup_tasks(
            f"""id,parent_id,text,status
            6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t0,in_progress
            033f3ae4-659d-47ff-a53b-e2579a9a643c,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t1,in_progress
            53a6485e-3473-49bd-bc9d-2fe1d3a9707e,033f3ae4-659d-47ff-a53b-e2579a9a643c,t1.1,in_progress
            f0a8399e-4941-407d-aba5-1312d16c2ed8,53a6485e-3473-49bd-bc9d-2fe1d3a9707e,t1.1.1,not_started
            a5da4c15-8fa7-4948-8549-3d3c14f903f4,53a6485e-3473-49bd-bc9d-2fe1d3a9707e,t1.1.2,completed
            c8c453d8-349f-4ac6-a061-8a16973b09b8,033f3ae4-659d-47ff-a53b-e2579a9a643c,t1.2,completed
            a7789f7d-08f0-45e7-97b4-d091f3132d53,c8c453d8-349f-4ac6-a061-8a16973b09b8,t1.2.1,completed
            29aa2bca-ad56-4219-8f8e-b4d73d37789d,c8c453d8-349f-4ac6-a061-8a16973b09b8,t1.2.2,completed
            56f60eca-7821-44c2-a32e-46ff05d117f3,c8c453d8-349f-4ac6-a061-8a16973b09b8,t1.2.3,completed
            0406b08b-711e-4cc8-8698-987b4ea5a4c2,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t2,completed
            00089b83-c081-4767-97cc-d3b14c14654d,0406b08b-711e-4cc8-8698-987b4ea5a4c2,t2.1,completed
            d628712f-be7f-4b9a-87c4-61a6e8b37041,00089b83-c081-4767-97cc-d3b14c14654d,t2.1.1,completed
            bdbf2b33-8d12-490b-8b81-ceee91f53afb,0406b08b-711e-4cc8-8698-987b4ea5a4c2,t2.2,completed
            """
        )

        t1_1_2.transition_to('in_progress')
        t1_2_2.transition_to('in_progress')
        t2_1_1.transition_to('in_progress')

        self._refresh_from_db(
            g0, t0, t1, t1_1, t1_1_1, t1_1_2, t1_2, t1_2_1, t1_2_2, t1_2_3,
            t2, t2_1, t2_1_1, t2_2, g1, g2
        )
        self.assertEqual(g0.status, 'in_progress')
        self.assertEqual(t0.status, 'in_progress')
        self.assertEqual(t1.status, 'in_progress')
        self.assertEqual(t1_1.status, 'in_progress')
        self.assertEqual(t1_1_1.status, 'not_started')
        self.assertEqual(t1_1_2.status, 'in_progress')
        self.assertEqual(t1_2.status, 'in_progress')
        self.assertEqual(t1_2_1.status, 'completed')
        self.assertEqual(t1_2_2.status, 'in_progress')
        self.assertEqual(t1_2_3.status, 'completed')
        self.assertEqual(t2.status, 'in_progress')
        self.assertEqual(t2_1.status, 'in_progress')
        self.assertEqual(t2_1_1.status, 'in_progress')
        self.assertEqual(t2_2.status, 'completed')
        self.assertEqual(g1.status, 'in_progress')
        self.assertEqual(g2.status, 'completed')

    def test_transition_from_in_progress_to_not_started(self):
        """
        g0__in_progress
        ├── t0__not_started
        └── t1__in_progress
            ├── t1.1__in_progress
            │   └── t1.1.1__in_progress
            │   └── t1.1.2__in_progress
            └── t1.2__in_progress
                ├── t1.2.1__in_progress
                └── t1.2.2__not_started

        Transition t1.1.1: in_progress -> not_started
        Transition t1.2.1: in_progress -> not_started

        g0__in_progress
        ├── t0__not_started
        └── t1__in_progress
            ├── t1.1__in_progress
            │   └── t1.1.1__not_started
            │   └── t1.1.2__in_progress
            └── t1.2__not_started
                ├── t1.2.1__not_started
                └── t1.2.2__not_started
        """
        g0 = Goal.objects.create(
            id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472',
            status='in_progress',
        )
        (
            t0, t1, t1_1, t1_1_1, t1_1_2, t1_2, t1_2_1, t1_2_2,
        ) = setup_tasks(
            """id,parent_id,text,status
            6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t0,not_started
            d628712f-be7f-4b9a-87c4-61a6e8b37041,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t1,in_progress
            53a6485e-3473-49bd-bc9d-2fe1d3a9707e,d628712f-be7f-4b9a-87c4-61a6e8b37041,t1.1,in_progress
            033f3ae4-659d-47ff-a53b-e2579a9a643c,53a6485e-3473-49bd-bc9d-2fe1d3a9707e,t1.1.1,in_progress
            c8c453d8-349f-4ac6-a061-8a16973b09b8,53a6485e-3473-49bd-bc9d-2fe1d3a9707e,t1.1.2,in_progress
            00089b83-c081-4767-97cc-d3b14c14654d,d628712f-be7f-4b9a-87c4-61a6e8b37041,t1.2,in_progress
            f0a8399e-4941-407d-aba5-1312d16c2ed8,00089b83-c081-4767-97cc-d3b14c14654d,t1.2.1,in_progress
            a5da4c15-8fa7-4948-8549-3d3c14f903f4,00089b83-c081-4767-97cc-d3b14c14654d,t1.2.2,not_started
            """
        )

        self.assertEqual(t1_2_2.status, 'not_started')
        self.assertEqual(t1_2_1.status, 'in_progress')
        self.assertEqual(t1_2.status, 'in_progress')
        self.assertEqual(t1_1_2.status, 'in_progress')
        self.assertEqual(t1_1_1.status, 'in_progress')
        self.assertEqual(t1_1.status, 'in_progress')
        self.assertEqual(t1.status, 'in_progress')
        self.assertEqual(t0.status, 'not_started')
        self.assertEqual(g0.status, 'in_progress')

        t1_1_1.transition_to('not_started')

        self._refresh_from_db(
            t0, t1, t1_1, t1_1_1, t1_1_2, t1_2, t1_2_1, t1_2_2,
        )

        t1_2_1.transition_to('not_started')

        self._refresh_from_db(
            t0, t1, t1_1, t1_1_1, t1_1_2, t1_2, t1_2_1, t1_2_2,
        )
        self.assertEqual(t1_2_2.status, 'not_started')
        self.assertEqual(t1_2_1.status, 'not_started')
        self.assertEqual(t1_2.status, 'not_started')
        self.assertEqual(t1_1_2.status, 'in_progress')
        self.assertEqual(t1_1_1.status, 'not_started')
        self.assertEqual(t1_1.status, 'in_progress')
        self.assertEqual(t1.status, 'in_progress')
        self.assertEqual(t0.status, 'not_started')
        self.assertEqual(g0.status, 'in_progress')

    def test_transition_parent(self):
        """
        g0__not_started
        ├── t0__not_started
        │   └── t0_1__not_started
        │       └── t0_1_1__not_started
        ├── t1__in_progress
        │   └── t1_1__in_progress
        │       └── t1_1_1__in_progress
        └── t2__completed
            └── t2_1__completed
                └── t2_1_1__completed
        """
        Goal.objects.create(
            id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472',
            status='not_started',
        )
        (
            t0,
            t0_1,
            t0_1_1,
            t1,
            t1_1,
            t1_1_1,
            t2,
            t2_1,
            t2_1_1,
        ) = setup_tasks(
            """id,parent_id,text,status
            6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t0,not_started
            d628712f-be7f-4b9a-87c4-61a6e8b37041,6a844440-13a1-48fc-9974-0b0f2114eafa,t0.1,not_started
            56f60eca-7821-44c2-a32e-46ff05d117f3,d628712f-be7f-4b9a-87c4-61a6e8b37041,t0.1.1,not_started
            033f3ae4-659d-47ff-a53b-e2579a9a643c,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t1,in_progress
            53a6485e-3473-49bd-bc9d-2fe1d3a9707e,033f3ae4-659d-47ff-a53b-e2579a9a643c,t1.1,in_progress
            c8c453d8-349f-4ac6-a061-8a16973b09b8,53a6485e-3473-49bd-bc9d-2fe1d3a9707e,t1.1.1,in_progress
            00089b83-c081-4767-97cc-d3b14c14654d,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t2,completed
            f0a8399e-4941-407d-aba5-1312d16c2ed8,00089b83-c081-4767-97cc-d3b14c14654d,t2.1,completed
            a5da4c15-8fa7-4948-8549-3d3c14f903f4,f0a8399e-4941-407d-aba5-1312d16c2ed8,t2.1.1,completed
            """
        )

        with self.assertRaises(InvalidStatusTransition):
            t0.transition_to('in_progress')

        with self.assertRaises(InvalidStatusTransition):
            t0_1.transition_to('in_progress')

        with self.assertRaises(InvalidStatusTransition):
            t1.transition_to('completed')

        with self.assertRaises(InvalidStatusTransition):
            t1_1.transition_to('completed')

        with self.assertRaises(InvalidStatusTransition):
            t2.transition_to('in_progress')

        with self.assertRaises(InvalidStatusTransition):
            t2_1.transition_to('in_progress')

        self.assertEqual(t0.status, 'not_started')
        self.assertEqual(t0_1.status, 'not_started')
        self.assertEqual(t0_1_1.status, 'not_started')
        self.assertEqual(t1.status, 'in_progress')
        self.assertEqual(t1_1.status, 'in_progress')
        self.assertEqual(t1_1_1.status, 'in_progress')
        self.assertEqual(t2.status, 'completed')
        self.assertEqual(t2_1.status, 'completed')
        self.assertEqual(t2_1_1.status, 'completed')

    def test_transition_jump(self):
        """
        g0__not_started
        └── t0__not_started
        """
        g0 = Goal.objects.create(
            id='e2617ee8-19e1-4f3a-9874-7c6bba6cd472',
            status='not_started',
        )
        (t0,) = setup_tasks(
            f"""id,parent_id,text,status
            6a844440-13a1-48fc-9974-0b0f2114eafa,e2617ee8-19e1-4f3a-9874-7c6bba6cd472,t0,not_started
            """
        )

        with self.assertRaises(InvalidStatusTransition):
            t0.transition_to('completed')

        self.assertEqual(t0.status, 'not_started')
        self.assertEqual(g0.status, 'not_started')

    def _refresh_from_db(self, *args):
        for model in args:
            model.refresh_from_db()
