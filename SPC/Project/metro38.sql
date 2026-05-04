--
-- PostgreSQL database dump
--

\restrict BOghsXo3ne3WGlefKT2Cdeaad5QKdtgKQesbjB0HkrhCnPHVZcigRvwEQbeiU3u

-- Dumped from database version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)

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
-- Name: check_route_station(); Type: FUNCTION; Schema: public; Owner: abhishek
--

CREATE FUNCTION public.check_route_station() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM trains t
        JOIN route_stations rs 
        ON t.route_id = rs.route_id
        WHERE t.train_id = NEW.train_id
        AND rs.station_id = NEW.station_id
    ) THEN
        RAISE EXCEPTION 'Station does not belong to train route';
    END IF;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.check_route_station() OWNER TO abhishek;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: route_stations; Type: TABLE; Schema: public; Owner: abhishek
--

CREATE TABLE public.route_stations (
    id integer NOT NULL,
    route_id integer,
    station_id integer,
    station_order integer NOT NULL,
    distance_km double precision
);


ALTER TABLE public.route_stations OWNER TO abhishek;

--
-- Name: route_stations_id_seq; Type: SEQUENCE; Schema: public; Owner: abhishek
--

CREATE SEQUENCE public.route_stations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.route_stations_id_seq OWNER TO abhishek;

--
-- Name: route_stations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: abhishek
--

ALTER SEQUENCE public.route_stations_id_seq OWNED BY public.route_stations.id;


--
-- Name: routes; Type: TABLE; Schema: public; Owner: abhishek
--

CREATE TABLE public.routes (
    route_id integer NOT NULL,
    route_name character varying(50) NOT NULL
);


ALTER TABLE public.routes OWNER TO abhishek;

--
-- Name: routes_route_id_seq; Type: SEQUENCE; Schema: public; Owner: abhishek
--

CREATE SEQUENCE public.routes_route_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.routes_route_id_seq OWNER TO abhishek;

--
-- Name: routes_route_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: abhishek
--

ALTER SEQUENCE public.routes_route_id_seq OWNED BY public.routes.route_id;


--
-- Name: stations; Type: TABLE; Schema: public; Owner: abhishek
--

CREATE TABLE public.stations (
    station_id integer NOT NULL,
    station_name character varying(50) NOT NULL
);


ALTER TABLE public.stations OWNER TO abhishek;

--
-- Name: stations_station_id_seq; Type: SEQUENCE; Schema: public; Owner: abhishek
--

CREATE SEQUENCE public.stations_station_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stations_station_id_seq OWNER TO abhishek;

--
-- Name: stations_station_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: abhishek
--

ALTER SEQUENCE public.stations_station_id_seq OWNED BY public.stations.station_id;


--
-- Name: train_schedule; Type: TABLE; Schema: public; Owner: abhishek
--

CREATE TABLE public.train_schedule (
    schedule_id integer NOT NULL,
    train_id integer,
    station_id integer,
    arrival_time time without time zone,
    departure_time time without time zone,
    platform_no integer
);


ALTER TABLE public.train_schedule OWNER TO abhishek;

--
-- Name: train_schedule_schedule_id_seq; Type: SEQUENCE; Schema: public; Owner: abhishek
--

ALTER TABLE public.train_schedule ALTER COLUMN schedule_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.train_schedule_schedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: trains; Type: TABLE; Schema: public; Owner: abhishek
--

CREATE TABLE public.trains (
    train_id integer NOT NULL,
    train_name character varying(50),
    route_id integer,
    direction text
);


ALTER TABLE public.trains OWNER TO abhishek;

--
-- Name: trains_train_id_seq; Type: SEQUENCE; Schema: public; Owner: abhishek
--

CREATE SEQUENCE public.trains_train_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trains_train_id_seq OWNER TO abhishek;

--
-- Name: trains_train_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: abhishek
--

ALTER SEQUENCE public.trains_train_id_seq OWNED BY public.trains.train_id;


--
-- Name: route_stations id; Type: DEFAULT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.route_stations ALTER COLUMN id SET DEFAULT nextval('public.route_stations_id_seq'::regclass);


--
-- Name: routes route_id; Type: DEFAULT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.routes ALTER COLUMN route_id SET DEFAULT nextval('public.routes_route_id_seq'::regclass);


--
-- Name: stations station_id; Type: DEFAULT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.stations ALTER COLUMN station_id SET DEFAULT nextval('public.stations_station_id_seq'::regclass);


--
-- Name: trains train_id; Type: DEFAULT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.trains ALTER COLUMN train_id SET DEFAULT nextval('public.trains_train_id_seq'::regclass);


--
-- Data for Name: route_stations; Type: TABLE DATA; Schema: public; Owner: abhishek
--

COPY public.route_stations (id, route_id, station_id, station_order, distance_km) FROM stdin;
1	1	1	1	\N
2	1	2	2	\N
3	1	3	3	\N
4	1	4	4	\N
5	1	5	5	\N
6	1	6	6	\N
7	1	7	7	\N
8	1	8	8	\N
9	1	9	9	\N
10	1	10	10	\N
11	1	11	11	\N
12	1	12	12	\N
13	1	13	13	\N
14	1	14	14	\N
15	1	15	15	\N
16	1	16	16	\N
17	2	28	1	\N
18	2	29	2	\N
19	2	30	3	\N
20	2	31	4	\N
21	2	32	5	\N
22	2	33	6	\N
23	2	34	7	\N
24	2	35	8	\N
25	2	36	9	\N
26	2	37	10	\N
27	2	9	11	\N
28	2	39	12	\N
29	2	40	13	\N
30	2	41	14	\N
\.


--
-- Data for Name: routes; Type: TABLE DATA; Schema: public; Owner: abhishek
--

COPY public.routes (route_id, route_name) FROM stdin;
1	Aqua Line
2	Purple Line
\.


--
-- Data for Name: stations; Type: TABLE DATA; Schema: public; Owner: abhishek
--

COPY public.stations (station_id, station_name) FROM stdin;
1	Vanaz
2	Anand Nagar
3	Ideal Colony
4	Nal Stop
5	Garware College
6	Deccan Gymkhana
7	Chhatrapati Sambhaji Udyan
8	PMC
9	Civil Court
10	Mangalwar Peth
11	Pune Railway Station
12	Ruby Hall Clinic
13	Bund Garden
14	Yerawada
15	Kalyani Nagar
16	Ramwadi
28	PCMC
29	Sant Tukaram Nagar
30	Bhosari
31	Kasarwadi
32	Phugewadi
33	Dapodi
34	Bopodi
35	Khadki
36	Range Hills
37	Shivajinagar
39	Budhwar Peth
40	Mandai
41	Swargate
\.


--
-- Data for Name: train_schedule; Type: TABLE DATA; Schema: public; Owner: abhishek
--

COPY public.train_schedule (schedule_id, train_id, station_id, arrival_time, departure_time, platform_no) FROM stdin;
49	3	28	06:12:00	06:13:00	1
50	3	29	06:15:00	06:16:00	1
51	3	30	06:18:00	06:19:00	1
52	3	31	06:21:00	06:22:00	1
53	3	32	06:24:00	06:25:00	1
54	3	33	06:27:00	06:28:00	1
55	3	34	06:30:00	06:31:00	1
56	3	35	06:33:00	06:34:00	1
57	3	36	06:36:00	06:37:00	1
58	3	37	06:39:00	06:40:00	1
59	3	9	06:42:00	06:43:00	1
60	3	39	06:45:00	06:46:00	1
61	3	40	06:48:00	06:49:00	1
62	3	41	06:51:00	06:52:00	1
17	1	1	06:00:00	06:01:00	1
18	1	2	06:03:00	06:04:00	1
19	1	3	06:06:00	06:07:00	1
20	1	4	06:09:00	06:10:00	1
21	1	5	06:12:00	06:13:00	1
22	1	6	06:15:00	06:16:00	1
23	1	7	06:18:00	06:19:00	1
24	1	8	06:21:00	06:22:00	1
25	1	9	06:24:00	06:25:00	1
26	1	10	06:27:00	06:28:00	1
27	1	11	06:30:00	06:31:00	1
28	1	12	06:33:00	06:34:00	1
29	1	13	06:36:00	06:37:00	1
30	1	14	06:39:00	06:40:00	1
31	1	15	06:42:00	06:43:00	1
32	1	16	06:45:00	06:46:00	1
33	2	1	06:06:00	06:07:00	2
34	2	2	06:09:00	06:10:00	2
35	2	3	06:12:00	06:13:00	2
36	2	4	06:15:00	06:16:00	2
37	2	5	06:18:00	06:19:00	2
38	2	6	06:21:00	06:22:00	2
39	2	7	06:24:00	06:25:00	2
40	2	8	06:27:00	06:28:00	2
41	2	9	06:30:00	06:31:00	2
42	2	10	06:33:00	06:34:00	2
43	2	11	06:36:00	06:37:00	2
44	2	12	06:39:00	06:40:00	2
45	2	13	06:42:00	06:43:00	2
46	2	14	06:45:00	06:46:00	2
47	2	15	06:48:00	06:49:00	2
48	2	16	06:51:00	06:52:00	2
\.


--
-- Data for Name: trains; Type: TABLE DATA; Schema: public; Owner: abhishek
--

COPY public.trains (train_id, train_name, route_id, direction) FROM stdin;
1	Aqua_1	1	UP
3	Purple_1	2	UP
4	Purple_2	2	DOWN
2	Aqua_2	1	DOWN
\.


--
-- Name: route_stations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: abhishek
--

SELECT pg_catalog.setval('public.route_stations_id_seq', 30, true);


--
-- Name: routes_route_id_seq; Type: SEQUENCE SET; Schema: public; Owner: abhishek
--

SELECT pg_catalog.setval('public.routes_route_id_seq', 2, true);


--
-- Name: stations_station_id_seq; Type: SEQUENCE SET; Schema: public; Owner: abhishek
--

SELECT pg_catalog.setval('public.stations_station_id_seq', 41, true);


--
-- Name: train_schedule_schedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: abhishek
--

SELECT pg_catalog.setval('public.train_schedule_schedule_id_seq', 62, true);


--
-- Name: trains_train_id_seq; Type: SEQUENCE SET; Schema: public; Owner: abhishek
--

SELECT pg_catalog.setval('public.trains_train_id_seq', 4, true);


--
-- Name: route_stations route_stations_pkey; Type: CONSTRAINT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.route_stations
    ADD CONSTRAINT route_stations_pkey PRIMARY KEY (id);


--
-- Name: routes routes_pkey; Type: CONSTRAINT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_pkey PRIMARY KEY (route_id);


--
-- Name: routes routes_route_name_key; Type: CONSTRAINT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_route_name_key UNIQUE (route_name);


--
-- Name: stations stations_pkey; Type: CONSTRAINT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.stations
    ADD CONSTRAINT stations_pkey PRIMARY KEY (station_id);


--
-- Name: stations stations_station_name_key; Type: CONSTRAINT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.stations
    ADD CONSTRAINT stations_station_name_key UNIQUE (station_name);


--
-- Name: train_schedule train_schedule_pkey; Type: CONSTRAINT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.train_schedule
    ADD CONSTRAINT train_schedule_pkey PRIMARY KEY (schedule_id);


--
-- Name: trains trains_pkey; Type: CONSTRAINT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.trains
    ADD CONSTRAINT trains_pkey PRIMARY KEY (train_id);


--
-- Name: route_stations route_stations_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.route_stations
    ADD CONSTRAINT route_stations_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.routes(route_id);


--
-- Name: route_stations route_stations_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.route_stations
    ADD CONSTRAINT route_stations_station_id_fkey FOREIGN KEY (station_id) REFERENCES public.stations(station_id);


--
-- Name: train_schedule train_schedule_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.train_schedule
    ADD CONSTRAINT train_schedule_station_id_fkey FOREIGN KEY (station_id) REFERENCES public.stations(station_id);


--
-- Name: train_schedule train_schedule_train_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.train_schedule
    ADD CONSTRAINT train_schedule_train_id_fkey FOREIGN KEY (train_id) REFERENCES public.trains(train_id);


--
-- Name: trains trains_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: abhishek
--

ALTER TABLE ONLY public.trains
    ADD CONSTRAINT trains_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.routes(route_id);


--
-- PostgreSQL database dump complete
--

\unrestrict BOghsXo3ne3WGlefKT2Cdeaad5QKdtgKQesbjB0HkrhCnPHVZcigRvwEQbeiU3u

