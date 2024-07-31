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
-- Name: members_id_member_seq; Type: SEQUENCE SET; Schema: public; Owner: queue_db_admin
--

SELECT pg_catalog.setval('public.members_id_member_seq', 1, true);


--
-- Name: queuesubjects_id_queue_seq; Type: SEQUENCE SET; Schema: public; Owner: queue_db_admin
--

SELECT pg_catalog.setval('public.queuesubjects_id_queue_seq', 1, true);


--
-- Name: subjects_id_subject_seq; Type: SEQUENCE SET; Schema: public; Owner: queue_db_admin
--

SELECT pg_catalog.setval('public.subjects_id_subject_seq', 1, true);


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