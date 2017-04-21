from __future__ import unicode_literals


from django.test import TestCase
from SNe.models import SN, Project
from Comments.models import Comment
from django.contrib import auth

User=auth.get_user_model()

class SNModelTest(TestCase):

    def test_default_test(self):
        sn=SN()
        self.assertEqual(sn.sn_name, '')
        self.assertEqual(sn.ra, 0.0)
        self.assertEqual(sn.dec, 0.0)

    def test_can_create_object(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        self.assertEqual(sn, SN.objects.first())

    def test_get_absolute_url(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        self.assertIn(sn.get_absolute_url(), '/sn/%d/' % (sn.id))

    def test_sn_can_have_multiple_co_is(self):
        pi=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        coi1=User.objects.create_user(email='coi@test.com', password="blabla", first_name="CoTest")
        coi2=User.objects.create_user(email='coi2@test.com', password="blablabla", first_name="Co2Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=pi)
        sn.coinvestigators.add(coi1)
        sn.coinvestigators.add(coi2)
        sn.save()
        self.assertEqual(sn.coinvestigators.count(), 2)
        self.assertEqual(sn.coinvestigators.all()[0], coi1)

    def test_sn_can_have_type_z_and_host(self):
        pi=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=pi, sntype="II-P", host="NGC 1234", z=0.01)
        self.assertEqual(sn.sntype, "II-P")

    def test_sn_can_have_comments(self):
        pi=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=pi, sntype="II-P", host="NGC 1234", z=0.01)
        comment=Comment.objects.create(text="Bla", author=pi)
        sn.comments.add(comment)
        sn.save()
        self.assertEqual(sn.comments.count(),1)
        self.assertEqual(sn.comments.first(), comment)

class ProjectModelTest(TestCase):

    def test_can_create_object(self):
        project=Project.objects.create(title="Bla", description="Bla bla bla")
        self.assertEqual(project, Project.objects.first())

    def test_project_can_have_multiple_co_is(self):
        pi=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        coi1=User.objects.create_user(email='coi@test.com', password="blabla", first_name="CoTest")
        coi2=User.objects.create_user(email='coi2@test.com', password="blablabla", first_name="Co2Test")
        project=Project.objects.create(title="Bla", pi=pi)
        project.coinvestigators.add(coi1)
        project.coinvestigators.add(coi2)
        project.save()
        self.assertEqual(project.coinvestigators.count(), 2)
        self.assertEqual(project.coinvestigators.all()[0], coi1)

    def test_project_can_have_multiple_SNe(self):
        pi=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn1=SN.objects.create(sn_name='SN 2017A', pi=pi)
        sn2=SN.objects.create(sn_name="SN 2018B", pi=pi)
        project=Project.objects.create(title="Bla", pi=pi)
        project.sne.add(sn1)
        project.sne.add(sn2)
        project.save()
        self.assertEqual(project.sne.count(), 2)
        self.assertEqual(project.sne.all()[0], sn1)

    def test_project_has_absolute_url(self):
        project=Project.objects.create(title="Bla")
        self.assertEqual(project.get_absolute_url(), '/projects/%d/' % (project.id))

    def test_project_can_have_comments(self):
        pi=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        project=Project.objects.create(title="Bla", pi=pi)
        comment=Comment.objects.create(text="Bla", author=pi)
        project.comments.add(comment)
        project.save()
        self.assertEqual(project.comments.count(),1)
        self.assertEqual(project.comments.first(), comment)
