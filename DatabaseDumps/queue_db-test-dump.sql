--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1
-- Dumped by pg_dump version 15.1


--CREATE DATABASE queue_db_test
--    WITH
--    OWNER = queue_db_admin
--    ENCODING = 'UTF8'
--    LC_COLLATE = 'Russian_Russia.1251'
--    LC_CTYPE = 'Russian_Russia.1251'
--    TABLESPACE = pg_default
--    CONNECTION LIMIT = -1
--    IS_TEMPLATE = False;

CREATE ROLE queue_db_admin WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  CREATEDB
  NOCREATEROLE
  NOREPLICATION
  ENCRYPTED PASSWORD 'SCRAM-SHA-256$4096:0g5+Hrr/X0fTf0QT1/u3LA==$BG3fu+N3EVn82BStFSLqlRxOX/BJjaSYuEpNTtxIS+Q=:e/E6dtlZ4JoIP/TYpiwXPe4l3tbfLQnraXUBDZ96gTk=';

GRANT pg_monitor TO queue_db_admin;

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.queuesubjects DROP CONSTRAINT IF EXISTS "QueueSubjects_Subjects_fk";
ALTER TABLE IF EXISTS ONLY public.queuemembers DROP CONSTRAINT IF EXISTS "QueueMembers_QueueSubjects_fk";
ALTER TABLE IF EXISTS ONLY public.queuemembers DROP CONSTRAINT IF EXISTS "QueueMembers_Members_fk";
ALTER TABLE IF EXISTS ONLY public.subjects DROP CONSTRAINT IF EXISTS subjects_title_key;
ALTER TABLE IF EXISTS ONLY public.members DROP CONSTRAINT IF EXISTS members_tg_num_key;
ALTER TABLE IF EXISTS ONLY public.subjects DROP CONSTRAINT IF EXISTS "Subjects_pk";
ALTER TABLE IF EXISTS ONLY public.queuesubjects DROP CONSTRAINT IF EXISTS "QueueSubjects_pk";
ALTER TABLE IF EXISTS ONLY public.members DROP CONSTRAINT IF EXISTS "Members_pk";
ALTER TABLE IF EXISTS public.subjects ALTER COLUMN id_subject DROP DEFAULT;
ALTER TABLE IF EXISTS public.queuesubjects ALTER COLUMN id_queue DROP DEFAULT;
ALTER TABLE IF EXISTS public.members ALTER COLUMN id_member DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.subjects_id_subject_seq;
DROP TABLE IF EXISTS public.subjects;
DROP SEQUENCE IF EXISTS public.queuesubjects_id_queue_seq;
DROP TABLE IF EXISTS public.queuesubjects;
DROP TABLE IF EXISTS public.queuemembers;
DROP SEQUENCE IF EXISTS public.members_id_member_seq;
DROP TABLE IF EXISTS public.members;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: members; Type: TABLE; Schema: public; Owner: queue_db_admin
--

CREATE TABLE public.members (
    id_member integer NOT NULL,
    name character varying NOT NULL,
    tg_num character varying NOT NULL
);


ALTER TABLE public.members OWNER TO queue_db_admin;

--
-- Name: members_id_member_seq; Type: SEQUENCE; Schema: public; Owner: queue_db_admin
--

CREATE SEQUENCE public.members_id_member_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.members_id_member_seq OWNER TO queue_db_admin;

--
-- Name: members_id_member_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: queue_db_admin
--

ALTER SEQUENCE public.members_id_member_seq OWNED BY public.members.id_member;


--
-- Name: queuemembers; Type: TABLE; Schema: public; Owner: queue_db_admin
--

CREATE TABLE public.queuemembers (
    queue_id integer NOT NULL,
    member_id integer NOT NULL,
    entry_time timestamp without time zone NOT NULL,
    place_number integer NOT NULL,
    entry_type character varying NOT NULL
);


ALTER TABLE public.queuemembers OWNER TO queue_db_admin;

--
-- Name: queuesubjects; Type: TABLE; Schema: public; Owner: queue_db_admin
--

CREATE TABLE public.queuesubjects (
    id_queue integer NOT NULL,
    subject_id integer NOT NULL,
    is_last boolean NOT NULL
);


ALTER TABLE public.queuesubjects OWNER TO queue_db_admin;

--
-- Name: queuesubjects_id_queue_seq; Type: SEQUENCE; Schema: public; Owner: queue_db_admin
--

CREATE SEQUENCE public.queuesubjects_id_queue_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.queuesubjects_id_queue_seq OWNER TO queue_db_admin;

--
-- Name: queuesubjects_id_queue_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: queue_db_admin
--

ALTER SEQUENCE public.queuesubjects_id_queue_seq OWNED BY public.queuesubjects.id_queue;


--
-- Name: subjects; Type: TABLE; Schema: public; Owner: queue_db_admin
--

CREATE TABLE public.subjects (
    id_subject integer NOT NULL,
    title character varying NOT NULL
);


ALTER TABLE public.subjects OWNER TO queue_db_admin;

--
-- Name: subjects_id_subject_seq; Type: SEQUENCE; Schema: public; Owner: queue_db_admin
--

CREATE SEQUENCE public.subjects_id_subject_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_id_subject_seq OWNER TO queue_db_admin;

--
-- Name: subjects_id_subject_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: queue_db_admin
--

ALTER SEQUENCE public.subjects_id_subject_seq OWNED BY public.subjects.id_subject;


--
-- Name: members id_member; Type: DEFAULT; Schema: public; Owner: queue_db_admin
--

ALTER TABLE ONLY public.members ALTER COLUMN id_member SET DEFAULT nextval('public.members_id_member_seq'::regclass);


--
-- Name: queuesubjects id_queue; Type: DEFAULT; Schema: public; Owner: queue_db_admin
--

ALTER TABLE ONLY public.queuesubjects ALTER COLUMN id_queue SET DEFAULT nextval('public.queuesubjects_id_queue_seq'::regclass);


--
-- Name: subjects id_subject; Type: DEFAULT; Schema: public; Owner: queue_db_admin
--

ALTER TABLE ONLY public.subjects ALTER COLUMN id_subject SET DEFAULT nextval('public.subjects_id_subject_seq'::regclass);


--
-- Data for Name: members; Type: TABLE DATA; Schema: public; Owner: queue_db_admin
--

INSERT INTO public.members (id_member, name, tg_num) VALUES (1, 'artas', '123456');
INSERT INTO public.members (id_member, name, tg_num) VALUES (2, 'dmitry', '789101112');
INSERT INTO public.members (id_member, name, tg_num) VALUES (3, 'artem', '1314151617');


--
-- Data for Name: subjects; Type: TABLE DATA; Schema: public; Owner: queue_db_admin
--

INSERT INTO public.subjects (id_subject, title) VALUES (1, 'trkpo');
INSERT INTO public.subjects (id_subject, title) VALUES (2, 'oprkppim');
INSERT INTO public.subjects (id_subject, title) VALUES (3, 'pdpu');


--
-- Data for Name: queuesubjects; Type: TABLE DATA; Schema: public; Owner: queue_db_admin
--

INSERT INTO public.queuesubjects (id_queue, subject_id, is_last) VALUES (1, 1, false);
INSERT INTO public.queuesubjects (id_queue, subject_id, is_last) VALUES (2, 2, false);
INSERT INTO public.queuesubjects (id_queue, subject_id, is_last) VALUES (3, 3, true);


--
-- Data for Name: queuemembers; Type: TABLE DATA; Schema: public; Owner: queue_db_admin
--

INSERT INTO public.queuemembers (queue_id, member_id, entry_time, place_number, entry_type) VALUES (1, 1, '2024-02-18 23:19:16.334518', 1, 0);
INSERT INTO public.queuemembers (queue_id, member_id, entry_time, place_number, entry_type) VALUES (1, 2, '2024-02-18 23:20:16.334518', 2, 0);
INSERT INTO public.queuemembers (queue_id, member_id, entry_time, place_number, entry_type) VALUES (1, 3, '2024-02-18 23:21:16.334518', 3, 0);
INSERT INTO public.queuemembers (queue_id, member_id, entry_time, place_number, entry_type) VALUES (2, 1, '2024-02-18 23:34:16.334518', 3, 2);
INSERT INTO public.queuemembers (queue_id, member_id, entry_time, place_number, entry_type) VALUES (2, 3, '2024-02-18 23:38:16.334518', 2, 1);


--
-- Name: members_id_member_seq; Type: SEQUENCE SET; Schema: public; Owner: queue_db_admin
--

SELECT pg_catalog.setval('public.members_id_member_seq', 4, true);


--
-- Name: queuesubjects_id_queue_seq; Type: SEQUENCE SET; Schema: public; Owner: queue_db_admin
--

SELECT pg_catalog.setval('public.queuesubjects_id_queue_seq', 4, true);


--
-- Name: subjects_id_subject_seq; Type: SEQUENCE SET; Schema: public; Owner: queue_db_admin
--

SELECT pg_catalog.setval('public.subjects_id_subject_seq', 4, true);


--
-- Name: members Members_pk; Type: CONSTRAINT; Schema: public; Owner: queue_db_admin
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT "Members_pk" PRIMARY KEY (id_member);


--
-- Name: queuesubjects QueueSubjects_pk; Type: CONSTRAINT; Schema: public; Owner: queue_db_admin
--

ALTER TABLE ONLY public.queuesubjects
    ADD CONSTRAINT "QueueSubjects_pk" PRIMARY KEY (id_queue);


--
-- Name: subjects Subjects_pk; Type: CONSTRAINT; Schema: public; Owner: queue_db_admin
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT "Subjects_pk" PRIMARY KEY (id_subject);


--
-- Name: members members_tg_num_key; Type: CONSTRAINT; Schema: public; Owner: queue_db_admin
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_tg_num_key UNIQUE (tg_num);


--
-- Name: subjects subjects_title_key; Type: CONSTRAINT; Schema: public; Owner: queue_db_admin
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_title_key UNIQUE (title);


--
-- Name: queuemembers QueueMembers_Members_fk; Type: FK CONSTRAINT; Schema: public; Owner: queue_db_admin
--

ALTER TABLE ONLY public.queuemembers
    ADD CONSTRAINT "QueueMembers_Members_fk" FOREIGN KEY (member_id) REFERENCES public.members(id_member) ON DELETE CASCADE;


--
-- Name: queuemembers QueueMembers_QueueSubjects_fk; Type: FK CONSTRAINT; Schema: public; Owner: queue_db_admin
--

ALTER TABLE ONLY public.queuemembers
    ADD CONSTRAINT "QueueMembers_QueueSubjects_fk" FOREIGN KEY (queue_id) REFERENCES public.queuesubjects(id_queue) ON DELETE CASCADE;


--
-- Name: queuesubjects QueueSubjects_Subjects_fk; Type: FK CONSTRAINT; Schema: public; Owner: queue_db_admin
--

ALTER TABLE ONLY public.queuesubjects
    ADD CONSTRAINT "QueueSubjects_Subjects_fk" FOREIGN KEY (subject_id) REFERENCES public.subjects(id_subject);


--
-- PostgreSQL database dump complete
--

