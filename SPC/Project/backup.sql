--
-- PostgreSQL database dump
--

\restrict RAxb7592BFb8POqpPlw1gOpYuXSTcVYgCHqttjj7wBEhRk2ekWQW2mlNFasUImG

-- Dumped from database version 18.1 (Debian 18.1-2)
-- Dumped by pg_dump version 18.1 (Debian 18.1-2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: line_config; Type: TABLE; Schema: public; Owner: matrix
--

CREATE TABLE public.line_config (
    route_id integer,
    frequency_minutes integer,
    turnaround_minutes integer
);


ALTER TABLE public.line_config OWNER TO matrix;

--
-- Name: route_stations; Type: TABLE; Schema: public; Owner: matrix
--

CREATE TABLE public.route_stations (
    id integer NOT NULL,
    route_id integer,
    station_id integer,
    station_order integer NOT NULL,
    distance_km double precision
);


ALTER TABLE public.route_stations OWNER TO matrix;

--
-- Name: route_stations_id_seq; Type: SEQUENCE; Schema: public; Owner: matrix
--

CREATE SEQUENCE public.route_stations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.route_stations_id_seq OWNER TO matrix;

--
-- Name: route_stations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: matrix
--

ALTER SEQUENCE public.route_stations_id_seq OWNED BY public.route_stations.id;


--
-- Name: routes; Type: TABLE; Schema: public; Owner: matrix
--

CREATE TABLE public.routes (
    route_id integer NOT NULL,
    route_name character varying(50) NOT NULL
);


ALTER TABLE public.routes OWNER TO matrix;

--
-- Name: routes_route_id_seq; Type: SEQUENCE; Schema: public; Owner: matrix
--

CREATE SEQUENCE public.routes_route_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.routes_route_id_seq OWNER TO matrix;

--
-- Name: routes_route_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: matrix
--

ALTER SEQUENCE public.routes_route_id_seq OWNED BY public.routes.route_id;


--
-- Name: schedule; Type: TABLE; Schema: public; Owner: matrix
--

CREATE TABLE public.schedule (
    schedule_id integer NOT NULL,
    train_id integer,
    start_time time without time zone,
    end_time time without time zone
);


ALTER TABLE public.schedule OWNER TO matrix;

--
-- Name: schedule_schedule_id_seq; Type: SEQUENCE; Schema: public; Owner: matrix
--

CREATE SEQUENCE public.schedule_schedule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.schedule_schedule_id_seq OWNER TO matrix;

--
-- Name: schedule_schedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: matrix
--

ALTER SEQUENCE public.schedule_schedule_id_seq OWNED BY public.schedule.schedule_id;


--
-- Name: segment_schedule; Type: TABLE; Schema: public; Owner: matrix
--

CREATE TABLE public.segment_schedule (
    id integer NOT NULL,
    train_id integer,
    from_station integer,
    to_station integer,
    start_time time without time zone,
    end_time time without time zone
);


ALTER TABLE public.segment_schedule OWNER TO matrix;

--
-- Name: segment_schedule_id_seq; Type: SEQUENCE; Schema: public; Owner: matrix
--

CREATE SEQUENCE public.segment_schedule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.segment_schedule_id_seq OWNER TO matrix;

--
-- Name: segment_schedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: matrix
--

ALTER SEQUENCE public.segment_schedule_id_seq OWNED BY public.segment_schedule.id;


--
-- Name: signals; Type: TABLE; Schema: public; Owner: matrix
--

CREATE TABLE public.signals (
    segment_id integer,
    signal_status character varying(10)
);


ALTER TABLE public.signals OWNER TO matrix;

--
-- Name: station_intervals; Type: TABLE; Schema: public; Owner: matrix
--

CREATE TABLE public.station_intervals (
    route_id integer,
    from_station integer,
    to_station integer,
    travel_time_min double precision
);


ALTER TABLE public.station_intervals OWNER TO matrix;

--
-- Name: station_timing; Type: TABLE; Schema: public; Owner: matrix
--

CREATE TABLE public.station_timing (
    train_id integer,
    station_id integer,
    arrival_time time without time zone,
    departure_time time without time zone
);


ALTER TABLE public.station_timing OWNER TO matrix;

--
-- Name: stations; Type: TABLE; Schema: public; Owner: matrix
--

CREATE TABLE public.stations (
    station_id integer NOT NULL,
    station_name character varying(50) NOT NULL,
    lat double precision,
    lng double precision
);


ALTER TABLE public.stations OWNER TO matrix;

--
-- Name: stations_station_id_seq; Type: SEQUENCE; Schema: public; Owner: matrix
--

CREATE SEQUENCE public.stations_station_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stations_station_id_seq OWNER TO matrix;

--
-- Name: stations_station_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: matrix
--

ALTER SEQUENCE public.stations_station_id_seq OWNED BY public.stations.station_id;


--
-- Name: track_segments; Type: TABLE; Schema: public; Owner: matrix
--

CREATE TABLE public.track_segments (
    segment_id integer NOT NULL,
    from_station integer,
    to_station integer,
    route_id integer
);


ALTER TABLE public.track_segments OWNER TO matrix;

--
-- Name: track_segments_segment_id_seq; Type: SEQUENCE; Schema: public; Owner: matrix
--

CREATE SEQUENCE public.track_segments_segment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.track_segments_segment_id_seq OWNER TO matrix;

--
-- Name: track_segments_segment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: matrix
--

ALTER SEQUENCE public.track_segments_segment_id_seq OWNED BY public.track_segments.segment_id;


--
-- Name: train_status; Type: TABLE; Schema: public; Owner: matrix
--

CREATE TABLE public.train_status (
    train_id integer,
    current_station integer,
    next_station integer,
    status character varying(20),
    last_updated timestamp without time zone
);


ALTER TABLE public.train_status OWNER TO matrix;

--
-- Name: trains; Type: TABLE; Schema: public; Owner: matrix
--

CREATE TABLE public.trains (
    train_id integer NOT NULL,
    train_name character varying(50),
    route_id integer
);


ALTER TABLE public.trains OWNER TO matrix;

--
-- Name: trains_train_id_seq; Type: SEQUENCE; Schema: public; Owner: matrix
--

CREATE SEQUENCE public.trains_train_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trains_train_id_seq OWNER TO matrix;

--
-- Name: trains_train_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: matrix
--

ALTER SEQUENCE public.trains_train_id_seq OWNED BY public.trains.train_id;


--
-- Name: route_stations id; Type: DEFAULT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.route_stations ALTER COLUMN id SET DEFAULT nextval('public.route_stations_id_seq'::regclass);


--
-- Name: routes route_id; Type: DEFAULT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.routes ALTER COLUMN route_id SET DEFAULT nextval('public.routes_route_id_seq'::regclass);


--
-- Name: schedule schedule_id; Type: DEFAULT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.schedule ALTER COLUMN schedule_id SET DEFAULT nextval('public.schedule_schedule_id_seq'::regclass);


--
-- Name: segment_schedule id; Type: DEFAULT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.segment_schedule ALTER COLUMN id SET DEFAULT nextval('public.segment_schedule_id_seq'::regclass);


--
-- Name: stations station_id; Type: DEFAULT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.stations ALTER COLUMN station_id SET DEFAULT nextval('public.stations_station_id_seq'::regclass);


--
-- Name: track_segments segment_id; Type: DEFAULT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.track_segments ALTER COLUMN segment_id SET DEFAULT nextval('public.track_segments_segment_id_seq'::regclass);


--
-- Name: trains train_id; Type: DEFAULT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.trains ALTER COLUMN train_id SET DEFAULT nextval('public.trains_train_id_seq'::regclass);


--
-- Data for Name: line_config; Type: TABLE DATA; Schema: public; Owner: matrix
--

COPY public.line_config (route_id, frequency_minutes, turnaround_minutes) FROM stdin;
1	6	8
2	6	8
\.


--
-- Data for Name: route_stations; Type: TABLE DATA; Schema: public; Owner: matrix
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
-- Data for Name: routes; Type: TABLE DATA; Schema: public; Owner: matrix
--

COPY public.routes (route_id, route_name) FROM stdin;
1	Aqua Line
2	Purple Line
\.


--
-- Data for Name: schedule; Type: TABLE DATA; Schema: public; Owner: matrix
--

COPY public.schedule (schedule_id, train_id, start_time, end_time) FROM stdin;
1	1	09:00:00	10:00:00
2	2	09:10:00	10:10:00
3	3	09:05:00	10:05:00
4	4	09:15:00	10:15:00
\.


--
-- Data for Name: segment_schedule; Type: TABLE DATA; Schema: public; Owner: matrix
--

COPY public.segment_schedule (id, train_id, from_station, to_station, start_time, end_time) FROM stdin;
1	1	1	2	09:00:00	09:05:00
2	2	1	2	09:03:00	09:08:00
3	1	1	2	09:00:00	09:05:00
4	2	1	2	09:03:00	09:08:00
\.


--
-- Data for Name: signals; Type: TABLE DATA; Schema: public; Owner: matrix
--

COPY public.signals (segment_id, signal_status) FROM stdin;
1	GREEN
2	RED
\.


--
-- Data for Name: station_intervals; Type: TABLE DATA; Schema: public; Owner: matrix
--

COPY public.station_intervals (route_id, from_station, to_station, travel_time_min) FROM stdin;
1	1	2	5
\.


--
-- Data for Name: station_timing; Type: TABLE DATA; Schema: public; Owner: matrix
--

COPY public.station_timing (train_id, station_id, arrival_time, departure_time) FROM stdin;
1	1	09:00:00	09:01:00
1	2	09:03:00	09:04:00
1	3	09:06:00	09:07:00
1	4	09:09:00	09:10:00
1	5	09:12:00	09:13:00
1	6	09:15:00	09:16:00
1	7	09:18:00	09:19:00
1	8	09:21:00	09:22:00
1	9	09:24:00	09:25:00
1	10	09:27:00	09:28:00
1	1	09:00:00	09:01:00
1	2	09:03:00	09:04:00
1	3	09:06:00	09:07:00
1	4	09:09:00	09:10:00
1	5	09:12:00	09:13:00
1	6	09:15:00	09:16:00
1	7	09:18:00	09:19:00
1	8	09:21:00	09:22:00
1	9	09:24:00	09:25:00
1	10	09:27:00	09:28:00
\.


--
-- Data for Name: stations; Type: TABLE DATA; Schema: public; Owner: matrix
--

COPY public.stations (station_id, station_name, lat, lng) FROM stdin;
1	Vanaz	18.507101	73.805268
2	Anand Nagar	18.509576	73.814077
3	Ideal Colony	18.509016	73.822059
4	Nal Stop	18.507339	73.828703
5	Garware College	18.512015	73.838061
6	Deccan Gymkhana	18.516309	73.844385
7	Chhatrapati Sambhaji Udyan	18.520157	73.847545
8	PMC	18.52277	73.853505
10	Mangalwar Peth	18.53007	73.864819
11	Pune Railway Station	18.529652	73.872627
12	Ruby Hall Clinic	18.532708	73.877859
13	Bund Garden	18.540778	73.88357
14	Yerawada	18.54534	73.886678
15	Kalyani Nagar	18.544315	73.905647
16	Ramwadi	18.557484	73.909043
28	PCMC	18.629364	73.803338
29	Sant Tukaram Nagar	18.608923	73.820203
30	Bhosari	18.609396	73.820136
31	Kasarwadi	18.599667	73.827226
32	Phugewadi	18.591131	73.831216
33	Dapodi	18.583751	73.833831
34	Bopodi	18.570061	73.838036
35	Khadki	18.562358	73.842098
36	Range Hills	18.549971	73.845935
37	Shivajinagar	18.532477	73.849212
9	Civil Court	18.526817	73.857868
39	Budhwar Peth	18.521515	73.859691
40	Mandai	18.512609	73.857428
41	Swargate	18.500903	73.857065
\.


--
-- Data for Name: track_segments; Type: TABLE DATA; Schema: public; Owner: matrix
--

COPY public.track_segments (segment_id, from_station, to_station, route_id) FROM stdin;
1	28	29	2
2	29	30	2
3	30	31	2
4	31	32	2
5	32	33	2
6	33	34	2
7	34	35	2
8	35	36	2
9	36	37	2
10	37	9	2
11	9	39	2
12	39	40	2
13	40	41	2
14	1	2	1
15	2	3	1
16	3	4	1
17	4	5	1
18	5	6	1
19	6	7	1
20	7	8	1
21	8	9	1
22	9	10	1
23	10	11	1
24	11	12	1
25	12	13	1
26	13	14	1
27	14	15	1
28	15	16	1
\.


--
-- Data for Name: train_status; Type: TABLE DATA; Schema: public; Owner: matrix
--

COPY public.train_status (train_id, current_station, next_station, status, last_updated) FROM stdin;
\.


--
-- Data for Name: trains; Type: TABLE DATA; Schema: public; Owner: matrix
--

COPY public.trains (train_id, train_name, route_id) FROM stdin;
1	Aqua_1	1
2	Aqua_2	1
3	Purple_1	2
4	Purple_2	2
\.


--
-- Name: route_stations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matrix
--

SELECT pg_catalog.setval('public.route_stations_id_seq', 30, true);


--
-- Name: routes_route_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matrix
--

SELECT pg_catalog.setval('public.routes_route_id_seq', 2, true);


--
-- Name: schedule_schedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matrix
--

SELECT pg_catalog.setval('public.schedule_schedule_id_seq', 4, true);


--
-- Name: segment_schedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matrix
--

SELECT pg_catalog.setval('public.segment_schedule_id_seq', 4, true);


--
-- Name: stations_station_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matrix
--

SELECT pg_catalog.setval('public.stations_station_id_seq', 41, true);


--
-- Name: track_segments_segment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matrix
--

SELECT pg_catalog.setval('public.track_segments_segment_id_seq', 28, true);


--
-- Name: trains_train_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matrix
--

SELECT pg_catalog.setval('public.trains_train_id_seq', 4, true);


--
-- Name: route_stations route_stations_pkey; Type: CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.route_stations
    ADD CONSTRAINT route_stations_pkey PRIMARY KEY (id);


--
-- Name: routes routes_pkey; Type: CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_pkey PRIMARY KEY (route_id);


--
-- Name: routes routes_route_name_key; Type: CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_route_name_key UNIQUE (route_name);


--
-- Name: schedule schedule_pkey; Type: CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.schedule
    ADD CONSTRAINT schedule_pkey PRIMARY KEY (schedule_id);


--
-- Name: segment_schedule segment_schedule_pkey; Type: CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.segment_schedule
    ADD CONSTRAINT segment_schedule_pkey PRIMARY KEY (id);


--
-- Name: stations stations_pkey; Type: CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.stations
    ADD CONSTRAINT stations_pkey PRIMARY KEY (station_id);


--
-- Name: stations stations_station_name_key; Type: CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.stations
    ADD CONSTRAINT stations_station_name_key UNIQUE (station_name);


--
-- Name: track_segments track_segments_pkey; Type: CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.track_segments
    ADD CONSTRAINT track_segments_pkey PRIMARY KEY (segment_id);


--
-- Name: trains trains_pkey; Type: CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.trains
    ADD CONSTRAINT trains_pkey PRIMARY KEY (train_id);


--
-- Name: route_stations route_stations_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.route_stations
    ADD CONSTRAINT route_stations_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.routes(route_id);


--
-- Name: route_stations route_stations_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.route_stations
    ADD CONSTRAINT route_stations_station_id_fkey FOREIGN KEY (station_id) REFERENCES public.stations(station_id);


--
-- Name: schedule schedule_train_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.schedule
    ADD CONSTRAINT schedule_train_id_fkey FOREIGN KEY (train_id) REFERENCES public.trains(train_id);


--
-- Name: segment_schedule segment_schedule_from_station_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.segment_schedule
    ADD CONSTRAINT segment_schedule_from_station_fkey FOREIGN KEY (from_station) REFERENCES public.stations(station_id);


--
-- Name: segment_schedule segment_schedule_to_station_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.segment_schedule
    ADD CONSTRAINT segment_schedule_to_station_fkey FOREIGN KEY (to_station) REFERENCES public.stations(station_id);


--
-- Name: segment_schedule segment_schedule_train_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.segment_schedule
    ADD CONSTRAINT segment_schedule_train_id_fkey FOREIGN KEY (train_id) REFERENCES public.trains(train_id);


--
-- Name: trains trains_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matrix
--

ALTER TABLE ONLY public.trains
    ADD CONSTRAINT trains_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.routes(route_id);


--
-- PostgreSQL database dump complete
--

\unrestrict RAxb7592BFb8POqpPlw1gOpYuXSTcVYgCHqttjj7wBEhRk2ekWQW2mlNFasUImG

