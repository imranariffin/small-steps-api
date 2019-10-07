from django.test import TestCase

from goals.models import Goal
from tasks.tests.helpers import setup_tasks


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
        pass

    def test_transition_from_in_progress_to_not_started(self):
        pass

    def test_transition_parent(self):
        for status_next in ['in_progress', 'completed']:
            pass

    def _refresh_from_db(self, *args):
        for model in args:
            model.refresh_from_db()
