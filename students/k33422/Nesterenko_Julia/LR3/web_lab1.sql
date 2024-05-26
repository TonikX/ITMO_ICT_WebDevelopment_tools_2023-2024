--
-- PostgreSQL database dump
--

-- Dumped from database version 14.11 (Homebrew)
-- Dumped by pg_dump version 16.0

-- Started on 2024-05-23 11:32:20 MSK

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
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: admin
--

-- CREATE SCHEMA public;

--
-- TOC entry 3724 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 837 (class 1247 OID 16693)
-- Name: accomodationtype; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.accomodationtype AS ENUM (
    'hotel',
    'hostel',
    'apartments',
    'couchsurfing',
    'tent'
);


--
-- TOC entry 855 (class 1247 OID 16757)
-- Name: gendertype; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.gendertype AS ENUM (
    'undefined',
    'female',
    'male'
);


--
-- TOC entry 849 (class 1247 OID 16743)
-- Name: statustype; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.statustype AS ENUM (
    'open',
    'closed',
    'cancelled'
);


--
-- TOC entry 843 (class 1247 OID 16713)
-- Name: transporttype; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.transporttype AS ENUM (
    'plane',
    'train',
    'ship',
    'ferry',
    'bus',
    'car',
    'motorbike',
    'bycicle',
    'walking',
    'hitchhiking'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 209 (class 1259 OID 16687)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);

--
-- TOC entry 211 (class 1259 OID 16704)
-- Name: stay; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.stay (
    location character varying NOT NULL,
    address character varying NOT NULL,
    accomodation public.accomodationtype NOT NULL,
    id integer NOT NULL
);

--
-- TOC entry 210 (class 1259 OID 16703)
-- Name: stay_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.stay_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- TOC entry 3726 (class 0 OID 0)
-- Dependencies: 210
-- Name: stay_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.stay_id_seq OWNED BY public.stay.id;


--
-- TOC entry 219 (class 1259 OID 16774)
-- Name: step; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.step (
    trip_id integer,
    date_from timestamp without time zone NOT NULL,
    date_to timestamp without time zone NOT NULL,
    est_price double precision NOT NULL,
    stay_id integer,
    transition_id integer,
    id integer NOT NULL
);

--
-- TOC entry 218 (class 1259 OID 16773)
-- Name: step_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.step_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- TOC entry 3727 (class 0 OID 0)
-- Dependencies: 218
-- Name: step_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.step_id_seq OWNED BY public.step.id;


--
-- TOC entry 213 (class 1259 OID 16734)
-- Name: transition; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.transition (
    location_from character varying NOT NULL,
    location_to character varying NOT NULL,
    transport public.transporttype NOT NULL,
    id integer NOT NULL
);

--
-- TOC entry 212 (class 1259 OID 16733)
-- Name: transition_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.transition_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- TOC entry 3728 (class 0 OID 0)
-- Dependencies: 212
-- Name: transition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.transition_id_seq OWNED BY public.transition.id;


--
-- TOC entry 215 (class 1259 OID 16750)
-- Name: trip; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trip (
    status public.statustype NOT NULL,
    member_capacity integer,
    id integer NOT NULL
);

--
-- TOC entry 214 (class 1259 OID 16749)
-- Name: trip_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trip_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3729 (class 0 OID 0)
-- Dependencies: 214
-- Name: trip_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trip_id_seq OWNED BY public.trip.id;


--
-- TOC entry 217 (class 1259 OID 16764)
-- Name: user; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."user" (
    username character varying NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    gender public.gendertype NOT NULL,
    age integer NOT NULL,
    telephone character varying NOT NULL,
    email character varying NOT NULL,
    bio character varying,
    id integer NOT NULL,
    password character varying NOT NULL,
    registered timestamp without time zone NOT NULL,
    is_admin boolean NOT NULL
);

--
-- TOC entry 216 (class 1259 OID 16763)
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- TOC entry 3730 (class 0 OID 0)
-- Dependencies: 216
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- TOC entry 221 (class 1259 OID 16796)
-- Name: usertriplink; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.usertriplink (
    user_id integer,
    trip_id integer,
    role character varying,
    id integer NOT NULL
);

--
-- TOC entry 220 (class 1259 OID 16795)
-- Name: usertriplink_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.usertriplink_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- TOC entry 3731 (class 0 OID 0)
-- Dependencies: 220
-- Name: usertriplink_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.usertriplink_id_seq OWNED BY public.usertriplink.id;


--
-- TOC entry 3539 (class 2604 OID 16707)
-- Name: stay id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.stay ALTER COLUMN id SET DEFAULT nextval('public.stay_id_seq'::regclass);


--
-- TOC entry 3543 (class 2604 OID 16777)
-- Name: step id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.step ALTER COLUMN id SET DEFAULT nextval('public.step_id_seq'::regclass);


--
-- TOC entry 3540 (class 2604 OID 16737)
-- Name: transition id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.transition ALTER COLUMN id SET DEFAULT nextval('public.transition_id_seq'::regclass);


--
-- TOC entry 3541 (class 2604 OID 16753)
-- Name: trip id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trip ALTER COLUMN id SET DEFAULT nextval('public.trip_id_seq'::regclass);


--
-- TOC entry 3542 (class 2604 OID 16767)
-- Name: user id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- TOC entry 3544 (class 2604 OID 16799)
-- Name: usertriplink id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.usertriplink ALTER COLUMN id SET DEFAULT nextval('public.usertriplink_id_seq'::regclass);


--
-- TOC entry 3706 (class 0 OID 16687)
-- Dependencies: 209
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.alembic_version (version_num) FROM stdin;
9c4b39bbb13b
\.


--
-- TOC entry 3708 (class 0 OID 16704)
-- Dependencies: 211
-- Data for Name: stay; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.stay (location, address, accomodation, id) FROM stdin;
Paris, France	Champs Elisees, 2	hotel	2
London, UK	Baker Street, 221B	apartments	3
New York, USA	Broadway, 8	hostel	4
Ponta Delgada, Portugal	Ponta Delgada, Portugal	apartments	23
Austin, Texas, US	Austin, Texas, US	apartments	24
Harlingen, Netherlands	Harlingen, Netherlands	apartments	25
Tervuren, Belgium	Tervuren, Belgium	apartments	26
Sutton, UK	Sutton, UK	apartments	27
Pembroke, UK	Pembroke, UK	apartments	28
Worstead, UK	Worstead, UK	apartments	29
Friskney, UK	Friskney, UK	apartments	30
Canterbury, UK	Canterbury, UK	apartments	31
Pembrokeshire, UK	Pembrokeshire, UK	apartments	32
Tietjerk, Netherlands	Tietjerk, Netherlands	apartments	33
The Haven, Billingshurst , UK	The Haven, Billingshurst , UK	apartments	34
Preston, UK	Preston, UK	apartments	35
Lincolnshire, UK	Lincolnshire, UK	apartments	36
Hatherton, UK	Hatherton, UK	apartments	37
Cockfield, UK	Cockfield, UK	apartments	38
Maidenwells, UK	Maidenwells, UK	apartments	39
Dirkshorn, Netherlands	Dirkshorn, Netherlands	apartments	40
Walterstone, UK	Walterstone, UK	apartments	41
Thorpe Morieux, UK	Thorpe Morieux, UK	apartments	42
Durban, South Africa	Blue Waters Hotel	hotel	43
Cairo, Egypt	Steigenberger Hotel El Tahrir Cairo	hotel	44
Marrakech, Morocco	Hôtel Racine	hotel	45
Zanzibar City, Tanzania	Tembo House Hotel	hotel	46
Tunis Centre Tunis, Tunisia	Hotel Carlton	hotel	47
Dubai, United Arab Emirates	FIVE Jumeirah Village	hotel	48
Makkah, Saudi Arabia	Swissotel Al Maqam Makkah	hotel	49
Narita, Japan	Narita Tobu Hotel Airport	hotel	50
Marina Bay, Singapore, Singapore	Marina Bay Sands	hotel	51
Qianjin District Kaohsiung, Taiwan	Skyone Hotel	hotel	52
Prague, Czech Republic	Don Giovanni Hotel Prague - Great Hotels of The World	hotel	53
Centro, Madrid, Spain	Riu Plaza España	hotel	54
Oslo, Norway	Citybox Oslo	hotel	55
Milbertshofen Am Hart, Munich, Germany	H2 Hotel München Olympiapark	hotel	56
Roissy-en-France, France	ibis Styles Paris Charles de Gaulle Airport	hotel	57
Hell's Kitchen, New York, NY United States	Pod Times Square	hotel	58
Venustiano Carranza, Mexico City, Mexico	Camino Real Aeropuerto	hotel	59
M5H Toronto, Canada	One King West Hotel and Residence	hotel	60
Bella Vista, Panama City, Panama	Riu Plaza Panamá	hotel	61
Santo Domingo, Dominican Republic	Catalonia Santo Domingo	hotel	62
Mascot, Sydney, Australia	Travelodge Hotel Sydney Airport	hotel	63
Wellington, New Zealand	James Cook Hotel Grand Chancellor	hotel	64
Nadi Nadi, Fiji	Fiji Gateway Hotel	hotel	65
Noumea, New Caledonia	Hotel Beaurivage	hotel	66
Bora Bora, French Polynesia	ROYAL BORA BORA	hotel	67
Guarulhos, CEP Brazil	Sleep Inn Aeroporto de Guarulhos - São Paulo	hotel	68
Santiago, Chile	La Quinta by Wyndham Santiago Aeropuerto	hotel	69
Fontibon, Bogotá, Colombia	Hotel Habitel Select	hotel	70
Callao, Callao Lima, Peru	Costa del Sol Wyndham Lima Airport	hotel	71
Punta Carretas, Montevideo, Uruguay	Dazzler by Wyndham Montevideo	hotel	72
Dubai Marina, Dubai	Papaya backpacker's	hostel	73
Beach Coast, Dubai	Berloga Capsule JBR	hostel	74
Beach Coast, Dubai	The White Stay	hostel	75
Deira, Dubai	VIP Hostel - Females Only	hostel	76
Beach Coast, Dubai	Travelers - Dubai Marina Hostel	hostel	77
Eilat, Israel	Little Prince Hostel-5 Min Walk To The Beach	hostel	78
Eilat, Israel	Exodus Hostel & Dive Center	hostel	79
Eilat, Israel	HI - Eilat Hostel	hostel	80
Eilat, Israel	Arava Hostel	hostel	81
Eilat, Israel	הבית הלבן של נתן	hostel	82
Amsterdam City Centre, Amsterdam	The Bee Hostel	hostel	83
Amsterdam City Centre, Amsterdam	THIS HO(S)TEL	hostel	84
Amsterdam City Centre, Amsterdam	Durty Nelly's Inn	hostel	85
Amsterdam City Centre, Amsterdam	Cocomama	hostel	86
Amsterdam City Centre, Amsterdam	Ecomama	hostel	87
Amsterdam, Netherlands	Via Amsterdam	hostel	88
Copenhagen, Denmark	Next House Copenhagen	hostel	89
Barcelona, Spain	Unite Hostel Barcelona	hostel	90
Copenhagen, Denmark	Steel House Copenhagen	hostel	91
Amsterdam, Netherlands	ClinkNOORD Hostel	hostel	92
New York, United States	HI New York City Hostel	hostel	93
Gaular, Norway	Gaular, Norway	apartments	94
Drimnin, UK	Drimnin, UK	apartments	95
Amsterdam, Netherlands	Amsterdam, Netherlands	apartments	96
\.


--
-- TOC entry 3716 (class 0 OID 16774)
-- Dependencies: 219
-- Data for Name: step; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.step (trip_id, date_from, date_to, est_price, stay_id, transition_id, id) FROM stdin;
3	2024-03-09 16:00:00	2024-03-09 17:15:00	100	\N	1	3
3	2024-03-09 18:00:00	2024-03-13 12:00:00	500	3	\N	4
3	2024-03-13 15:00:00	2024-03-13 22:00:00	0	\N	4	5
4	2024-05-10 19:50:00	2024-05-11 09:21:00	640	\N	3	6
\.


--
-- TOC entry 3710 (class 0 OID 16734)
-- Dependencies: 213
-- Data for Name: transition; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.transition (location_from, location_to, transport, id) FROM stdin;
Paris, France	London, UK	train	1
Paris, France	New York, USA	plane	2
London, UK	New York, USA	ship	3
London, UK	Manchester, UK	hitchhiking	4
London, UK	Dusseldorf	plane	5
London, UK	Sofia	plane	6
London, UK	Stuttgart	plane	7
London, UK	Warsaw	plane	8
London, UK	Paris	plane	9
London, UK	Mumbai	plane	10
London, UK	Jersey	plane	11
London, UK	Lyon	plane	12
London, UK	Nice	plane	13
London, UK	Brussels	plane	14
London, UK	New York City	plane	15
London, UK	Munich	plane	16
London, UK	New York City	plane	17
London, UK	Geneva	plane	18
London, UK	Marseille	plane	19
London, UK	Toronto	plane	20
London, UK	Belfast	plane	21
London, UK	New York City	plane	22
London, UK	Stockholm	plane	23
London, UK	Cairo	plane	24
London, UK	Casablanca	plane	25
London, UK	Dublin	plane	26
London, UK	Helsinki	plane	27
London, UK	Montreal	plane	28
London, UK	Amman	plane	29
London, UK	Glasgow	plane	30
London, UK	Naples	plane	31
London, UK	Amsterdam	plane	32
Buenos Aires, Argentina	Beijing, China	plane	33
Buenos Aires, Argentina	Athens, Greece	plane	34
Buenos Aires, Argentina	Thessaloniki, Greece	plane	35
Buenos Aires, Argentina	Mykonos, Greece	plane	36
Buenos Aires, Argentina	Santorini, Greece	plane	37
Buenos Aires, Argentina	Istanbul, Turkey	plane	38
Buenos Aires, Argentina	Berlin, Germany	plane	39
Buenos Aires, Argentina	Barcelona, Spain	plane	40
Buenos Aires, Argentina	Madrid, Spain	plane	41
Buenos Aires, Argentina	Lisbon, Portugal	plane	42
Buenos Aires, Argentina	Budapest, Hungary	plane	43
Buenos Aires, Argentina	Paris, France	plane	44
Buenos Aires, Argentina	Amsterdam, Netherlands	plane	45
Buenos Aires, Argentina	New York, USA	plane	46
Buenos Aires, Argentina	Miami, USA	plane	47
Buenos Aires, Argentina	Toronto, Canada	plane	48
Buenos Aires, Argentina	Dubai, UAE	plane	49
Istanbul	Dubrovnik, Croatia	ship	50
Venice	Dubrovnik, Croatia	ship	51
Ravenna	Dubrovnik, Croatia	ship	52
Rome	Dubrovnik, Croatia	ship	53
Malta	Dubrovnik, Croatia	ship	54
Southampton	Dubrovnik, Croatia	ship	55
Corfu	Dubrovnik, Croatia	ship	56
Trieste	Dubrovnik, Croatia	ship	57
London	Edinburgh	train	58
London	Manchester	train	59
London	Brighton	train	60
Glasgow	London	train	61
Edinburgh	London	train	62
London	Birmingham	train	63
London	Liverpool	train	64
Liverpool	London	train	65
London	Bath	train	66
Birmingham	London	train	67
London	Oxford	train	68
Newcastle	Glasgow	train	69
London	Leeds	train	70
London	Cardiff	train	71
London	Newcastle	train	72
Trains	Edinburgh	train	73
London	Paris	train	74
Paris	London	train	75
Milan	Venice	train	76
Barcelona	Madrid	train	77
Rome	Venice	train	78
London	Amsterdam	train	79
London	Brussels	train	80
Florence	Rome	train	81
Venice	Rome	train	82
Paris	Amsterdam	train	83
Brussels	Amsterdam	train	84
Madrid	Seville	train	85
Milan	Florence	train	86
Madrid	Barcelona	train	87
Florence	Venice	train	88
Dubrovnik	Dubrovnik, Croatia	ship	89
\.


--
-- TOC entry 3712 (class 0 OID 16750)
-- Dependencies: 215
-- Data for Name: trip; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trip (status, member_capacity, id) FROM stdin;
open	5	3
closed	1	4
\.


--
-- TOC entry 3714 (class 0 OID 16764)
-- Dependencies: 217
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public."user" (username, first_name, last_name, gender, age, telephone, email, bio, id, password, registered, is_admin) FROM stdin;
admin	Aaa	Aaaaa	undefined	30	77777777777	admin@example.com	best ever	1	$2b$12$Vq5k5t3RjuZvXR2ZFIhnreLK1JIKxq0kOXO787rC08TvLcnwC5Y4i	2024-03-06 13:32:09.116992	t
kate	Kate	Moss	female	50	98887779977	kate@example.com	model	3	$2b$12$h5VYvGEM8/kULqazBr4rVerbNYUAbAxMYG6.XOkdQcnJs5U6o2tk.	2024-03-07 23:05:16.125138	f
pepe	Pepe	The Frog	undefined	18	88005553535	pepe@example.com	the legend	4	$2b$12$G1nNYBpiHcRaKtV60YABa.X7Ga2uqAIGxtYwmqIFw9yzeW3qEoMOe	2024-03-07 23:05:16.125138	f
bob	Bob	Ross	male	65	79997779999	bob@example.com	painter	2	$2b$12$sYt.hi2jfs/nbrq8NtU8DeXDMjEPqAZR1i/NNCDzE6.LGV1AoAsDy	2024-03-07 23:05:16.125138	f
\.


--
-- TOC entry 3718 (class 0 OID 16796)
-- Dependencies: 221
-- Data for Name: usertriplink; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.usertriplink (user_id, trip_id, role, id) FROM stdin;
2	3	creator	3
3	3	translator	4
3	4	creator	5
\.


--
-- TOC entry 3732 (class 0 OID 0)
-- Dependencies: 210
-- Name: stay_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.stay_id_seq', 96, true);


--
-- TOC entry 3733 (class 0 OID 0)
-- Dependencies: 218
-- Name: step_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.step_id_seq', 6, true);


--
-- TOC entry 3734 (class 0 OID 0)
-- Dependencies: 212
-- Name: transition_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.transition_id_seq', 89, true);


--
-- TOC entry 3735 (class 0 OID 0)
-- Dependencies: 214
-- Name: trip_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trip_id_seq', 4, true);


--
-- TOC entry 3736 (class 0 OID 0)
-- Dependencies: 216
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.user_id_seq', 4, true);


--
-- TOC entry 3737 (class 0 OID 0)
-- Dependencies: 220
-- Name: usertriplink_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.usertriplink_id_seq', 5, true);


--
-- TOC entry 3546 (class 2606 OID 16691)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 3548 (class 2606 OID 16711)
-- Name: stay stay_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.stay
    ADD CONSTRAINT stay_pkey PRIMARY KEY (id);


--
-- TOC entry 3557 (class 2606 OID 16779)
-- Name: step step_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.step
    ADD CONSTRAINT step_pkey PRIMARY KEY (id);


--
-- TOC entry 3550 (class 2606 OID 16741)
-- Name: transition transition_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.transition
    ADD CONSTRAINT transition_pkey PRIMARY KEY (id);


--
-- TOC entry 3552 (class 2606 OID 16755)
-- Name: trip trip_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trip
    ADD CONSTRAINT trip_pkey PRIMARY KEY (id);


--
-- TOC entry 3559 (class 2606 OID 16805)
-- Name: usertriplink unique pair of ids; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.usertriplink
    ADD CONSTRAINT "unique pair of ids" UNIQUE (trip_id, user_id);


--
-- TOC entry 3555 (class 2606 OID 16771)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 3561 (class 2606 OID 16803)
-- Name: usertriplink usertriplink_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.usertriplink
    ADD CONSTRAINT usertriplink_pkey PRIMARY KEY (id);


--
-- TOC entry 3553 (class 1259 OID 16772)
-- Name: ix_user_username; Type: INDEX; Schema: public; Owner: admin
--

CREATE UNIQUE INDEX ix_user_username ON public."user" USING btree (username);


--
-- TOC entry 3562 (class 2606 OID 16816)
-- Name: step step_stay_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.step
    ADD CONSTRAINT step_stay_id_fkey FOREIGN KEY (stay_id) REFERENCES public.stay(id) ON DELETE CASCADE;


--
-- TOC entry 3563 (class 2606 OID 16821)
-- Name: step step_transition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.step
    ADD CONSTRAINT step_transition_id_fkey FOREIGN KEY (transition_id) REFERENCES public.transition(id) ON DELETE CASCADE;


--
-- TOC entry 3564 (class 2606 OID 16826)
-- Name: step step_trip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.step
    ADD CONSTRAINT step_trip_id_fkey FOREIGN KEY (trip_id) REFERENCES public.trip(id) ON DELETE CASCADE;


--
-- TOC entry 3565 (class 2606 OID 16836)
-- Name: usertriplink usertriplink_trip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.usertriplink
    ADD CONSTRAINT usertriplink_trip_id_fkey FOREIGN KEY (trip_id) REFERENCES public.trip(id) ON DELETE CASCADE;


--
-- TOC entry 3566 (class 2606 OID 16831)
-- Name: usertriplink usertriplink_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.usertriplink
    ADD CONSTRAINT usertriplink_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- TOC entry 3725 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: admin
--


-- Completed on 2024-05-23 11:32:20 MSK

--
-- PostgreSQL database dump complete
--

