--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.10
-- Dumped by pg_dump version 9.5.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: experiments; Type: TABLE; Schema: public; Owner: berrybed
--

CREATE TABLE experiments (
    eid integer NOT NULL,
    uid integer NOT NULL,
    title character varying(50) NOT NULL,
    description character varying(50),
    duration integer NOT NULL,
    created date,
    protocol character varying(50) NOT NULL,
    status character varying
);


ALTER TABLE experiments OWNER TO berrybed;

--
-- Name: experiments_eid_seq; Type: SEQUENCE; Schema: public; Owner: berrybed
--

CREATE SEQUENCE experiments_eid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE experiments_eid_seq OWNER TO berrybed;

--
-- Name: experiments_eid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: berrybed
--

ALTER SEQUENCE experiments_eid_seq OWNED BY experiments.eid;


--
-- Name: nodes; Type: TABLE; Schema: public; Owner: berrybed
--

CREATE TABLE nodes (
    nid integer NOT NULL,
    eid integer NOT NULL,
    name character varying(50),
    protocol character varying(50) NOT NULL,
    temperature integer,
    humdity integer
);


ALTER TABLE nodes OWNER TO berrybed;

--
-- Name: nodes_nid_seq; Type: SEQUENCE; Schema: public; Owner: berrybed
--

CREATE SEQUENCE nodes_nid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE nodes_nid_seq OWNER TO berrybed;

--
-- Name: nodes_nid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: berrybed
--

ALTER SEQUENCE nodes_nid_seq OWNED BY nodes.nid;


--
-- Name: results; Type: TABLE; Schema: public; Owner: berrybed
--

CREATE TABLE results (
    pid integer NOT NULL,
    eid integer NOT NULL,
    output text,
    res_id integer NOT NULL
);


ALTER TABLE results OWNER TO berrybed;

--
-- Name: results_res_id_seq; Type: SEQUENCE; Schema: public; Owner: berrybed
--

CREATE SEQUENCE results_res_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE results_res_id_seq OWNER TO berrybed;

--
-- Name: results_res_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: berrybed
--

ALTER SEQUENCE results_res_id_seq OWNED BY results.res_id;


--
-- Name: scenario; Type: TABLE; Schema: public; Owner: berrybed
--

CREATE TABLE scenario (
    pid integer NOT NULL,
    eid integer NOT NULL,
    en1 integer,
    en2 integer
);


ALTER TABLE scenario OWNER TO berrybed;

--
-- Name: scenario_pid_seq; Type: SEQUENCE; Schema: public; Owner: berrybed
--

CREATE SEQUENCE scenario_pid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE scenario_pid_seq OWNER TO berrybed;

--
-- Name: scenario_pid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: berrybed
--

ALTER SEQUENCE scenario_pid_seq OWNED BY scenario.pid;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE users (
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    pwdhash character varying(100) NOT NULL
);


ALTER TABLE users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: eid; Type: DEFAULT; Schema: public; Owner: berrybed
--

ALTER TABLE ONLY experiments ALTER COLUMN eid SET DEFAULT nextval('experiments_eid_seq'::regclass);


--
-- Name: nid; Type: DEFAULT; Schema: public; Owner: berrybed
--

ALTER TABLE ONLY nodes ALTER COLUMN nid SET DEFAULT nextval('nodes_nid_seq'::regclass);


--
-- Name: res_id; Type: DEFAULT; Schema: public; Owner: berrybed
--

ALTER TABLE ONLY results ALTER COLUMN res_id SET DEFAULT nextval('results_res_id_seq'::regclass);


--
-- Name: pid; Type: DEFAULT; Schema: public; Owner: berrybed
--

ALTER TABLE ONLY scenario ALTER COLUMN pid SET DEFAULT nextval('scenario_pid_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: experiments; Type: TABLE DATA; Schema: public; Owner: berrybed
--

COPY experiments (eid, uid, title, description, duration, created, protocol, status) FROM stdin;
1	1	test1	test1	300	2017-12-30	Zigbee	done
3	2	experiment1	phase2	30	2018-01-10	Zigbee	done
2	1	test1	test1	10000	2017-12-30	Zigbee	running
\.


--
-- Name: experiments_eid_seq; Type: SEQUENCE SET; Schema: public; Owner: berrybed
--

SELECT pg_catalog.setval('experiments_eid_seq', 3, true);


--
-- Data for Name: nodes; Type: TABLE DATA; Schema: public; Owner: berrybed
--

COPY nodes (nid, eid, name, protocol, temperature, humdity) FROM stdin;
2	1	rpi8	cord	0	0
1	1	rpi9	rott	10	0
3	1	rpi7	rott	0	10
4	3	rpi9	rott	5	2
5	3	rpi8	cord	0	0
6	3	rpi7	rott	10	4
\.


--
-- Name: nodes_nid_seq; Type: SEQUENCE SET; Schema: public; Owner: berrybed
--

SELECT pg_catalog.setval('nodes_nid_seq', 6, true);


--
-- Data for Name: results; Type: TABLE DATA; Schema: public; Owner: berrybed
--

COPY results (pid, eid, output, res_id) FROM stdin;
4	3	results/rpi9-3-4.csv	1
4	3	results/rpi8-3-4.csv	2
5	3	results/rpi7-3-5.csv	3
5	3	results/rpi8-3-5.csv	4
\.


--
-- Name: results_res_id_seq; Type: SEQUENCE SET; Schema: public; Owner: berrybed
--

SELECT pg_catalog.setval('results_res_id_seq', 4, true);


--
-- Data for Name: scenario; Type: TABLE DATA; Schema: public; Owner: berrybed
--

COPY scenario (pid, eid, en1, en2) FROM stdin;
2	1	1	2
3	1	3	2
4	3	4	5
5	3	6	5
\.


--
-- Name: scenario_pid_seq; Type: SEQUENCE SET; Schema: public; Owner: berrybed
--

SELECT pg_catalog.setval('scenario_pid_seq', 5, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (id, username, email, pwdhash) FROM stdin;
1	aziz	aziz@aziz.com	pbkdf2:sha256:50000$dqV7HTjJ$f329087d5adf33c49aa49a5ab41ca614b37f8d9943888c023dca4b1646026d2e
2	aziz2	azizaa@gmail.com	pbkdf2:sha256:50000$Ie0t4AbA$5d74a851dd5b32e3407daf714eeb9e56dae3f86762d8e80b90f0c15e3578b90b
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('users_id_seq', 2, true);


--
-- Name: experiments_pkey; Type: CONSTRAINT; Schema: public; Owner: berrybed
--

ALTER TABLE ONLY experiments
    ADD CONSTRAINT experiments_pkey PRIMARY KEY (eid);


--
-- Name: nodes_pkey; Type: CONSTRAINT; Schema: public; Owner: berrybed
--

ALTER TABLE ONLY nodes
    ADD CONSTRAINT nodes_pkey PRIMARY KEY (nid);


--
-- Name: scenario_pkey; Type: CONSTRAINT; Schema: public; Owner: berrybed
--

ALTER TABLE ONLY scenario
    ADD CONSTRAINT scenario_pkey PRIMARY KEY (pid);


--
-- Name: users_emaile_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_emaile_key UNIQUE (email);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

