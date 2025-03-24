--
-- File generated with SQLiteStudio v3.4.17 on Mon Mar 24 08:27:39 2025
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: chi_tiet_dv
DROP TABLE IF EXISTS chi_tiet_dv;
CREATE TABLE chi_tiet_dv (
    hd_id INTEGER,
    dv_id INTEGER,
    so_luong INTEGER,
    gia_luc_dat INTEGER,
    tong INTEGER,
    PRIMARY KEY (hd_id, dv_id),
    FOREIGN KEY (hd_id) REFERENCES hoa_don (hd_id),
    FOREIGN KEY (dv_id) REFERENCES dich_vu (dv_id)
);
INSERT INTO chi_tiet_dv (hd_id, dv_id, so_luong, gia_luc_dat, tong) VALUES (1, 1, 2, 15000, 30000);
INSERT INTO chi_tiet_dv (hd_id, dv_id, so_luong, gia_luc_dat, tong) VALUES (1, 3, 1, 20000, 20000);
INSERT INTO chi_tiet_dv (hd_id, dv_id, so_luong, gia_luc_dat, tong) VALUES (2, 2, 3, 25000, 75000);
INSERT INTO chi_tiet_dv (hd_id, dv_id, so_luong, gia_luc_dat, tong) VALUES (3, 4, 1, 50000, 50000);

-- Table: dat_phong
DROP TABLE IF EXISTS dat_phong;
CREATE TABLE dat_phong (
    booking_id INTEGER PRIMARY KEY,
    ngay_bd TEXT,
    ngay_kt TEXT,
    phi_dat_coc INTEGER,
    note TEXT,
    phong_id INTEGER,
    tien_luc_dat INTEGER,
    kh_id INTEGER,
    FOREIGN KEY (phong_id) REFERENCES phong (id),
    FOREIGN KEY (kh_id) REFERENCES khach_hang (kh_id)
);
INSERT INTO dat_phong (booking_id, ngay_bd, ngay_kt, phi_dat_coc, note, phong_id, tien_luc_dat, kh_id) VALUES (1, '2024-10-26', '2024-10-28', 100000, 'Kh�ch mu?n ph�ng c� view d?p', 101, 300000, 1);
INSERT INTO dat_phong (booking_id, ngay_bd, ngay_kt, phi_dat_coc, note, phong_id, tien_luc_dat, kh_id) VALUES (2, '2024-11-01', '2024-11-03', 150000, 'Kh�ch c?n th�m g?i', 202, 450000, 2);
INSERT INTO dat_phong (booking_id, ngay_bd, ngay_kt, phi_dat_coc, note, phong_id, tien_luc_dat, kh_id) VALUES (3, '2024-11-15', '2024-11-16', 200000, 'Ph�ng VIP cho gia d�nh', 301, 800000, 3);

-- Table: dich_vu
DROP TABLE IF EXISTS dich_vu;
CREATE TABLE dich_vu (
    dv_id INTEGER PRIMARY KEY,
    ten_dv TEXT,
    gia INTEGER
);
INSERT INTO dich_vu (dv_id, ten_dv, gia) VALUES (1, 'Nu?c ng?t', 15000);
INSERT INTO dich_vu (dv_id, ten_dv, gia) VALUES (2, 'Bia', 25000);
INSERT INTO dich_vu (dv_id, ten_dv, gia) VALUES (3, 'Snack', 20000);
INSERT INTO dich_vu (dv_id, ten_dv, gia) VALUES (4, 'Gi?t ?i', 50000);
INSERT INTO dich_vu (dv_id, ten_dv, gia) VALUES (5, 'abc', 10);

-- Table: gia_phong
DROP TABLE IF EXISTS gia_phong;
CREATE TABLE gia_phong (
    gia_id INTEGER PRIMARY KEY,
    ten_loai TEXT,
    gia_gio INTEGER,
    gia_ngay INTEGER,
    gia_dem INTEGER
);
INSERT INTO gia_phong (gia_id, ten_loai, gia_gio, gia_ngay, gia_dem) VALUES (1, 'Ph�ng �on', 50000, 300000, 400000);
INSERT INTO gia_phong (gia_id, ten_loai, gia_gio, gia_ngay, gia_dem) VALUES (2, 'Ph�ng ��i', 80000, 450000, 600000);
INSERT INTO gia_phong (gia_id, ten_loai, gia_gio, gia_ngay, gia_dem) VALUES (3, 'Ph�ng VIP', 150000, 800000, 1000000);

-- Table: hoa_don
DROP TABLE IF EXISTS hoa_don;
CREATE TABLE hoa_don (
    hd_id INTEGER PRIMARY KEY,
    tong_tien INTEGER,
    thoi_gian TEXT,
    nv_id INTEGER,
    thanh_toan_status INTEGER,
    FOREIGN KEY (nv_id) REFERENCES nhan_vien (nv_id)
);
INSERT INTO hoa_don (hd_id, tong_tien, thoi_gian, nv_id, thanh_toan_status) VALUES (1, 400000, '2024-10-28', 2, 1);
INSERT INTO hoa_don (hd_id, tong_tien, thoi_gian, nv_id, thanh_toan_status) VALUES (2, 600000, '2024-11-03', 2, 1);
INSERT INTO hoa_don (hd_id, tong_tien, thoi_gian, nv_id, thanh_toan_status) VALUES (3, 1000000, '2024-11-16', 3, 1);

-- Table: khach_hang
DROP TABLE IF EXISTS khach_hang;
CREATE TABLE khach_hang (kh_id INTEGER PRIMARY KEY, ten TEXT, sdt TEXT, image TEXT);
INSERT INTO khach_hang (kh_id, ten, sdt, image) VALUES (33, 'Doe aa', '123-456-7890', 'john.jpg');
INSERT INTO khach_hang (kh_id, ten, sdt, image) VALUES (34, 'aaazaaa', '1234', 'None');
INSERT INTO khach_hang (kh_id, ten, sdt, image) VALUES (36, 'Customer 36', '123-456-4951', NULL);

-- Table: nhan_vien
DROP TABLE IF EXISTS nhan_vien;
CREATE TABLE nhan_vien (
    nv_id INTEGER PRIMARY KEY,
    ten_nv TEXT,
    email TEXT,
    sdt TEXT,
    dia_chi TEXT,
    chuc_vu TEXT
);
INSERT INTO nhan_vien (nv_id, ten_nv, email, sdt, dia_chi, chuc_vu) VALUES (1, 'Ph?m Th? D', 'phamthi.d@example.com', '0909876543', '123 �u?ng X, Qu?n Y, TP.HCM', 'Qu?n l�');
INSERT INTO nhan_vien (nv_id, ten_nv, email, sdt, dia_chi, chuc_vu) VALUES (2, '�? Van E', 'dovan.e@example.com', '0918765432', '456 �u?ng Z, Qu?n T, H� N?i', 'L? t�n');
INSERT INTO nhan_vien (nv_id, ten_nv, email, sdt, dia_chi, chuc_vu) VALUES (3, 'Ho�ng Minh F', 'hoangminh.f@example.com', '0331234567', '789 �u?ng A, Qu?n B, �� N?ng', 'Nh�n Vi�n');

-- Table: phong
DROP TABLE IF EXISTS phong;
CREATE TABLE phong (id INTEGER PRIMARY KEY, ten_phong TEXT, so_giuong INTEGER, id_gia INTEGER, tinh_trang_dat_phong INTEGER DEFAULT (0), tinh_trang_su_dung INTEGER DEFAULT NULL, FOREIGN KEY (id_gia) REFERENCES gia_phong (gia_id));
INSERT INTO phong (id, ten_phong, so_giuong, id_gia, tinh_trang_dat_phong, tinh_trang_su_dung) VALUES (101, 'Ph�ng 101', 1, 1, 0, 1);
INSERT INTO phong (id, ten_phong, so_giuong, id_gia, tinh_trang_dat_phong, tinh_trang_su_dung) VALUES (102, 'Ph�ng 102', 2, 2, 0, 1);
INSERT INTO phong (id, ten_phong, so_giuong, id_gia, tinh_trang_dat_phong, tinh_trang_su_dung) VALUES (201, 'Ph�ng 201', 1, 1, 0, 1);
INSERT INTO phong (id, ten_phong, so_giuong, id_gia, tinh_trang_dat_phong, tinh_trang_su_dung) VALUES (202, 'Ph�ng 202', 2, 2, 0, 1);
INSERT INTO phong (id, ten_phong, so_giuong, id_gia, tinh_trang_dat_phong, tinh_trang_su_dung) VALUES (301, 'Ph�ng 301 VIP', 2, 3, 0, 0);

-- Table: user
DROP TABLE IF EXISTS user;
CREATE TABLE user (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    nv_id INTEGER,
    FOREIGN KEY (nv_id) REFERENCES nhan_vien (nv_id)
);
INSERT INTO user (user_id, username, password, nv_id) VALUES (1, 'admin', 'password123', NULL);
INSERT INTO user (user_id, username, password, nv_id) VALUES (2, 'letan1', 'letan456', 2);
INSERT INTO user (user_id, username, password, nv_id) VALUES (3, 'nhanvien1', 'nv789', 3);
INSERT INTO user (user_id, username, password, nv_id) VALUES (4, 'a', 'a', 2);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
