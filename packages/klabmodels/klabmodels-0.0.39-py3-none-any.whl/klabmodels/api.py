from datetime import datetime
from .models import Candidate, JobDescription, Interview, Questionnaire, CVEvaluation, Company
from langroid.agent.chat_document import ChatDocument
from typing import Dict, List
import logging
import time


def get_questionnaire_for_interview(candidate:str):
   """Extract list of questions for an interview"""

   pass

### Job Descriptions/Vacancies
def get_vacancy(vacancy_pk: str):
   try:
      vacancy = JobDescription.find(JobDescription.pk==vacancy_pk).first()
      vacancy.info(f"Vacancy {vacancy_pk} found")
      return vacancy
   except Exception:
     logging.error(f"Vacancy {vacancy_pk} not found.")


def persist_job_description(reference: str, title: str, company_name: str, **kwargs):
   """
   Persist a job description
   """
   try:
      # duplicated title
      if 'title' in kwargs: del kwargs['title']
      jd = JobDescription.find(JobDescription.reference==reference).first()
      logging.info(f"Found job: {reference}")
      jd.job_title = title
      jd.company = company_name
      if kwargs: jd.__dict__.update(kwargs)
   except:
      logging.info(f"Not Found job: {reference}")
      if 'job_title' in kwargs: kwargs.pop('job_title', None)
      jd = JobDescription(reference=reference, job_title=title, company=company_name, **kwargs)
   finally:
      jd.save()
   return jd



def get_jobs_descriptions(company: str):
   """
   Get Job Descriptions that have been processed to json format
   """
   #user = cl.user_session.get("account")
   try:
      jobs = JobDescription.find(JobDescription.company==company).all()
      if jobs:
        # some filter
        #jobs = [j for j in jobs if j.reference=='']
        return jobs
      else:
         logging.error(f"No jobs retrieved.")
   except Exception as e:
    logging.error(f"No jobs retrieved.")
    return None

### Candidates


def get_candidate(candidate_pk: str):
   try:
      candidate = Candidate.find(Candidate.pk==candidate_pk).first()
      logging.info(f"Candidate {candidate_pk} found")
      return candidate
   except Exception:
     logging.error(f"Candidate {candidate_pk} not found.")


def persist_candidate(name: str, **kwargs):
   """
   Persist a candidate
   """
   try:
      c = Candidate.find(Candidate.name==name).first()
      if 'name' in kwargs: del kwargs['name']
      c.__dict__.update(kwargs)
   except:
      c = Candidate(name=name, **kwargs)
   finally:
      c.save()
   return c
   
def get_candidates_job(job_reference: str):
   """
   Get candidates who have applied for a specific job
   """
   #user = cl.user_session.get("account")
   try:
      candidates = Candidate.find().all()
      if candidates:
        #candidates = [c for c in candidates if c.resume_classified] # CV has been processed
        candidates = [c for c in candidates if job_reference in c.jobs_applied] # Has applied for the job
        if candidates:
          return candidates
        else:
           logging.error(f"No candidates retrieved for the job position {job_reference}.")    
      else:
         logging.error(f"No candidates retrieved.")
   except Exception as e:
    logging.error(f"No candidates retrieved.")
    return None
   

def get_candidates_company(company: str):
   """
   Get candidates who have applied for a job at the company
   Args:
      company (str): company name
   """
   #user = cl.user_session.get("account")
   try:
      candidates = Candidate.find().all()
      jobs = JobDescription.find(JobDescription.company==company).all()
      if jobs:
         jobrefs = set([j.reference for j in jobs])
         #candidates = [c for c in candidates if c.resume_classified] # CV has been processed
         candidates = [c for c in candidates if set(c.jobs_applied) & jobrefs] # Has applied for jobs at the company
         if candidates:
            return candidates
         else:
           logging.error(f"No candidates retrieved for the job positions at  {company}.")    
      else:
         logging.error(f"No jobs advertised at company {company}.")
   except Exception as e:
    logging.error(f"No candidates retrieved.")
    return None


def apply_for_a_job(candidate_pk:str, job_reference: str):
  """
  A candidate applies for a job
  """
  try:
    candidate = Candidate.find(Candidate.pk==candidate_pk).first()
    if job_reference not in candidate.jobs_applied:
       candidate.jobs_applied.append(job_reference)
       candidate.save()
       logging.info(f"Candidate {candidate_pk} job application for job {job_reference} submitted.")
  except Exception:
     logging.error(f"Candidate {candidate_pk} not found.")


### Questionnaires


def create_interview(job: JobDescription, candidate: Candidate, questions: Questionnaire):
    """
    Save Interview questionnaire creation to Redis DB
    Args:
      job: (str) Job Description
      candidate: (Candidate) name and resume
      questions (Questionnaire): generated interview questions

    Returns: 
      interview:  interview id to be used to generate a link for the candidate interview
    """
    #user = cl.user_session.get("account")

    interview = Interview( 
                  date=time.time(), 
                  candidate=candidate.pk, 
                  job_description=job.pk,
                  questions=questions,
                  #uuid=interview_id
                  )
       
    interview.save()
    return interview


### Interviews 


def get_interview(interview_pk: str):
   try:
      interview = Interview.find(Interview.pk==interview_pk).first()
      logging.info(f"Interview {interview_pk} found")
      return interview
   except Exception:
     logging.error(f"Interview {interview_pk} not found.")


def persist_interview(interview_pk: str, **kwargs):
    """
    Save interview conversation into Interview object (existing)
    """
    #user = cl.user_session.get("account")
    try:
      interview = Interview.find(Interview.pk==interview_pk).first()
      if 'dialogue' in kwargs:
         dialogue = kwargs['dialogue'] 
         interview.interview =[msg for msg in dialogue if msg.role in ('user', 'assistant')]
         del kwargs['dialogue']
      if kwargs: interview.__dict__.update(kwargs)
      interview.save()
      logging.info(f"Interview saved for {interview.candidate} with {len(dialogue)} documents.")
    except Exception as e:
       logging.error(f"Error persisting interview: {str(e)}")


def get_interview_from_id(interview_id: str):
  """
  Retrieves stored interview
  """
  logging.info(f"Looking for interview {interview_id}")
  try:
    interview = Interview.find(Interview.pk==interview_id).first()
    return interview
  except Exception as e:
    logging.error(f"Interview {interview_id} not found")
    print(e)

def get_user_interviews(with_answers=True):
    """
    Retrieve generated questionnaires for a user
    """
    #user = cl.user_session.get("account")
    try:
      #interviews = Interview.find(Interview.user==user).all()
      interviews = Interview.find().all()
      logging.info(f"Retrieved {len(interviews)} interviews.")
      if interviews:
         if with_answers:
          i_list = [i for i in interviews if i.interview]
         else:
          i_list = [i for i in interviews if not i.interview]
         return i_list

    except Exception as e:
        logging.error(f"No interviews retrieved: {str(e)}")
        return None


def get_candidates_interviews_to_eval():
    """
    Retrieve generated questionnaires for a user
    """
    #user = cl.user_session.get("account")
    try:
      #interviews = Interview.find(Interview.user==user).all()
      interviews = Interview.find().all()
      interviews = [i for i in interviews if i.interview!=[]]
      logging.info(f"Retrieved {len(interviews)} interviews to evaluate")
      if interviews:
         candidates = [Candidate.find(Candidate.pk==i.candidate).first() for i in interviews]
         jobs = [JobDescription.find(JobDescription.pk==i.job_description).first() for i in interviews]
         return interviews, candidates, jobs
      else:
        logging.info(f"No interviews retrieved: {str(e)}")
        #return None

    except Exception as e:
        logging.error(f"No interviews retrieved: {str(e)}")
        #return None

### Interview Evaluations
def persist_interview_evaluation(interview_pk: str, evaluation: List[Dict]):
    """
    Store an interview evaluation on Redis
    """
    #user = cl.user_session.get("account")
    try:
      interview = Interview.find(Interview.pk==interview_pk).first()
      interview.evaluation = evaluation
      interview.save()
      logging.info(f"Interview evaluation saved for {interview.candidate}.")
    except Exception as e:
       logging.error(f"Error persisting interview: {str(e)}")



### CV Evaluations

def persist_cv_evaluation(candidate_pk: str, 
                          evaluation: Dict,
                          company: str=None, 
                          job_description: str=None):
   """
   Store a CV evaluation grading and summary on Redis
   """
   cv_evaluation = None
   
   evaluations = CVEvaluation.find(CVEvaluation.candidate==candidate_pk).all()
   if evaluations:

      if company: evaluations = [e for e in evaluations if e.company==company]
      if job_description: evaluations = [e for e in evaluations if e.jobdesc==job_description]
      # heuristic, always choose first one in case of multiple. Alternative, choose most recent
      cv_evaluation = evaluations[0]
      cv_evaluation.grade = evaluation.get('cv_overall_grade')
      cv_evaluation.summary = evaluation.get('summary')
      cv_evaluation.skills_evaluation = evaluation.get('skills_evaluation')

   else:
      logging.info(f"Adding CV evaluation for candidate {candidate_pk}...")
      cv_evaluation = CVEvaluation(candidate=candidate_pk,
                                   jobdesc=job_description,
                                   company = company,
                                   grade=evaluation.get('cv_overall_grade'),
                                   summary=evaluation.get('summary'),
                                   skills_evaluation=evaluation.get('skills_evaluation'))
   if cv_evaluation: cv_evaluation.save()
   return cv_evaluation
   

### Companies
def get_company(company_pk: str):
   try:
      company = Company.find(Company.pk==company_pk).first()
      company.info(f"Company {company_pk} found")
      return company
   except Exception:
     logging.error(f"Company {company_pk} not found.")


def persist_company(name: str, **kwargs):
   """
   Save Company info
   """
   try:
      company = Company.find(Company.name==name).first()
      logging.info(f"Found existing company {name}")
      company.__dict__.update(kwargs)
   except Exception as e:
      logging.info(f"Saving new company {name}: {str(e)}")
      company = Company(name=name, **kwargs)
   finally:
      company.save()
   return company

def getCompany(name: str):
   """
   Retrieve a company by name
   """
   try:
      company = Company.find(Company.name==name).first()
      return company
   except Exception as e:
      logging.info(f"Company {name} not found.")

def get_companies():
   """
   Retrieve companies
   """
   try:
      companies = Company.find().all()
      return companies
   except Exception as e:
      logging.info(f"No Company found.")
