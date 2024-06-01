--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Postgres.app)
-- Dumped by pg_dump version 16.2 (Homebrew)

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

--
-- Name: approvestatus; Type: TYPE; Schema: public; Owner: dptgo
--

CREATE TYPE public.approvestatus AS ENUM (
    'gathering',
    'completed',
    'pending',
    'approved',
    'rejected'
);


ALTER TYPE public.approvestatus OWNER TO dptgo;

--
-- Name: skill; Type: TYPE; Schema: public; Owner: dptgo
--

CREATE TYPE public.skill AS ENUM (
    'programming',
    'design',
    'data_analysis',
    'marketing',
    'management',
    'other'
);


ALTER TYPE public.skill OWNER TO dptgo;

--
-- Name: submissionstatus; Type: TYPE; Schema: public; Owner: dptgo
--

CREATE TYPE public.submissionstatus AS ENUM (
    'pending',
    'approved',
    'rejected'
);


ALTER TYPE public.submissionstatus OWNER TO dptgo;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: dptgo
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO dptgo;

--
-- Name: hackathon; Type: TABLE; Schema: public; Owner: dptgo
--

CREATE TABLE public.hackathon (
    title character varying NOT NULL,
    description character varying NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.hackathon OWNER TO dptgo;

--
-- Name: hackathon_id_seq; Type: SEQUENCE; Schema: public; Owner: dptgo
--

CREATE SEQUENCE public.hackathon_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hackathon_id_seq OWNER TO dptgo;

--
-- Name: hackathon_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dptgo
--

ALTER SEQUENCE public.hackathon_id_seq OWNED BY public.hackathon.id;


--
-- Name: participant; Type: TABLE; Schema: public; Owner: dptgo
--

CREATE TABLE public.participant (
    full_name character varying NOT NULL,
    nickname character varying NOT NULL,
    email character varying NOT NULL,
    phone character varying NOT NULL,
    skill public.skill NOT NULL,
    id integer NOT NULL,
    team_id integer
);


ALTER TABLE public.participant OWNER TO dptgo;

--
-- Name: participant_id_seq; Type: SEQUENCE; Schema: public; Owner: dptgo
--

CREATE SEQUENCE public.participant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.participant_id_seq OWNER TO dptgo;

--
-- Name: participant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dptgo
--

ALTER SEQUENCE public.participant_id_seq OWNED BY public.participant.id;


--
-- Name: submission; Type: TABLE; Schema: public; Owner: dptgo
--

CREATE TABLE public.submission (
    code character varying,
    file_url character varying,
    status public.submissionstatus NOT NULL,
    id integer NOT NULL,
    task_id integer NOT NULL,
    team_id integer NOT NULL
);


ALTER TABLE public.submission OWNER TO dptgo;

--
-- Name: submission_id_seq; Type: SEQUENCE; Schema: public; Owner: dptgo
--

CREATE SEQUENCE public.submission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.submission_id_seq OWNER TO dptgo;

--
-- Name: submission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dptgo
--

ALTER SEQUENCE public.submission_id_seq OWNED BY public.submission.id;


--
-- Name: task; Type: TABLE; Schema: public; Owner: dptgo
--

CREATE TABLE public.task (
    title character varying NOT NULL,
    description character varying NOT NULL,
    requirements character varying NOT NULL,
    evaluation_criteria character varying NOT NULL,
    id integer NOT NULL,
    hackathon_id integer NOT NULL
);


ALTER TABLE public.task OWNER TO dptgo;

--
-- Name: task_id_seq; Type: SEQUENCE; Schema: public; Owner: dptgo
--

CREATE SEQUENCE public.task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_id_seq OWNER TO dptgo;

--
-- Name: task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dptgo
--

ALTER SEQUENCE public.task_id_seq OWNED BY public.task.id;


--
-- Name: team; Type: TABLE; Schema: public; Owner: dptgo
--

CREATE TABLE public.team (
    name character varying NOT NULL,
    approve_status public.approvestatus NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.team OWNER TO dptgo;

--
-- Name: team_id_seq; Type: SEQUENCE; Schema: public; Owner: dptgo
--

CREATE SEQUENCE public.team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.team_id_seq OWNER TO dptgo;

--
-- Name: team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dptgo
--

ALTER SEQUENCE public.team_id_seq OWNED BY public.team.id;


--
-- Name: teamhackathon; Type: TABLE; Schema: public; Owner: dptgo
--

CREATE TABLE public.teamhackathon (
    team_id integer NOT NULL,
    hackathon_id integer NOT NULL,
    registration_date timestamp without time zone NOT NULL
);


ALTER TABLE public.teamhackathon OWNER TO dptgo;

--
-- Name: user; Type: TABLE; Schema: public; Owner: dptgo
--

CREATE TABLE public."user" (
    username character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public."user" OWNER TO dptgo;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: dptgo
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO dptgo;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dptgo
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: hackathon id; Type: DEFAULT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.hackathon ALTER COLUMN id SET DEFAULT nextval('public.hackathon_id_seq'::regclass);


--
-- Name: participant id; Type: DEFAULT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.participant ALTER COLUMN id SET DEFAULT nextval('public.participant_id_seq'::regclass);


--
-- Name: submission id; Type: DEFAULT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.submission ALTER COLUMN id SET DEFAULT nextval('public.submission_id_seq'::regclass);


--
-- Name: task id; Type: DEFAULT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.task ALTER COLUMN id SET DEFAULT nextval('public.task_id_seq'::regclass);


--
-- Name: team id; Type: DEFAULT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.team ALTER COLUMN id SET DEFAULT nextval('public.team_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: hackathon hackathon_pkey; Type: CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.hackathon
    ADD CONSTRAINT hackathon_pkey PRIMARY KEY (id);


--
-- Name: participant participant_pkey; Type: CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_pkey PRIMARY KEY (id);


--
-- Name: submission submission_pkey; Type: CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_pkey PRIMARY KEY (id);


--
-- Name: task task_pkey; Type: CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (id);


--
-- Name: team team_pkey; Type: CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_pkey PRIMARY KEY (id);


--
-- Name: teamhackathon teamhackathon_pkey; Type: CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.teamhackathon
    ADD CONSTRAINT teamhackathon_pkey PRIMARY KEY (team_id, hackathon_id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: participant participant_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.team(id);


--
-- Name: submission submission_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(id);


--
-- Name: submission submission_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.team(id);


--
-- Name: task task_hackathon_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_hackathon_id_fkey FOREIGN KEY (hackathon_id) REFERENCES public.hackathon(id);


--
-- Name: teamhackathon teamhackathon_hackathon_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.teamhackathon
    ADD CONSTRAINT teamhackathon_hackathon_id_fkey FOREIGN KEY (hackathon_id) REFERENCES public.hackathon(id);


--
-- Name: teamhackathon teamhackathon_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dptgo
--

ALTER TABLE ONLY public.teamhackathon
    ADD CONSTRAINT teamhackathon_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.team(id);


--
-- PostgreSQL database dump complete
--

