
// generated from codegen/templates/test_api.cpp

// stdlib
#include <stddef.h>
// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// emath
#include "emath.h"

#define TEST(X) if (!(X)){ PyErr_Format(PyExc_AssertionError, #X " (line %i)", __LINE__); return 0; };
#define TEST_OFFSET(X, N) TEST(offsetof(struct EMathApi, X) == (sizeof(size_t) + (sizeof(void *) * (N))));


static PyObject *
test_EMathApi_Get(PyObject *self, PyObject *args)
{
    struct EMathApi *api = EMathApi_Get();
    if (!api){ return 0; }
    TEST(!PyErr_Occurred());

    TEST(offsetof(struct EMathApi, version) == 0);
    TEST(api->version == 0);

    TEST_OFFSET(BVector1_GetType, 0);
    TEST_OFFSET(BVector1Array_GetType, 1);
    TEST_OFFSET(BVector1_Create, 2);
    TEST_OFFSET(BVector1Array_Create, 3);
    TEST_OFFSET(BVector1_GetValuePointer, 4);
    TEST_OFFSET(BVector1Array_GetValuePointer, 5);
    TEST_OFFSET(BVector1Array_GetLength, 6);

    TEST_OFFSET(DVector1_GetType, 7);
    TEST_OFFSET(DVector1Array_GetType, 8);
    TEST_OFFSET(DVector1_Create, 9);
    TEST_OFFSET(DVector1Array_Create, 10);
    TEST_OFFSET(DVector1_GetValuePointer, 11);
    TEST_OFFSET(DVector1Array_GetValuePointer, 12);
    TEST_OFFSET(DVector1Array_GetLength, 13);

    TEST_OFFSET(FVector1_GetType, 14);
    TEST_OFFSET(FVector1Array_GetType, 15);
    TEST_OFFSET(FVector1_Create, 16);
    TEST_OFFSET(FVector1Array_Create, 17);
    TEST_OFFSET(FVector1_GetValuePointer, 18);
    TEST_OFFSET(FVector1Array_GetValuePointer, 19);
    TEST_OFFSET(FVector1Array_GetLength, 20);

    TEST_OFFSET(I8Vector1_GetType, 21);
    TEST_OFFSET(I8Vector1Array_GetType, 22);
    TEST_OFFSET(I8Vector1_Create, 23);
    TEST_OFFSET(I8Vector1Array_Create, 24);
    TEST_OFFSET(I8Vector1_GetValuePointer, 25);
    TEST_OFFSET(I8Vector1Array_GetValuePointer, 26);
    TEST_OFFSET(I8Vector1Array_GetLength, 27);

    TEST_OFFSET(U8Vector1_GetType, 28);
    TEST_OFFSET(U8Vector1Array_GetType, 29);
    TEST_OFFSET(U8Vector1_Create, 30);
    TEST_OFFSET(U8Vector1Array_Create, 31);
    TEST_OFFSET(U8Vector1_GetValuePointer, 32);
    TEST_OFFSET(U8Vector1Array_GetValuePointer, 33);
    TEST_OFFSET(U8Vector1Array_GetLength, 34);

    TEST_OFFSET(I16Vector1_GetType, 35);
    TEST_OFFSET(I16Vector1Array_GetType, 36);
    TEST_OFFSET(I16Vector1_Create, 37);
    TEST_OFFSET(I16Vector1Array_Create, 38);
    TEST_OFFSET(I16Vector1_GetValuePointer, 39);
    TEST_OFFSET(I16Vector1Array_GetValuePointer, 40);
    TEST_OFFSET(I16Vector1Array_GetLength, 41);

    TEST_OFFSET(U16Vector1_GetType, 42);
    TEST_OFFSET(U16Vector1Array_GetType, 43);
    TEST_OFFSET(U16Vector1_Create, 44);
    TEST_OFFSET(U16Vector1Array_Create, 45);
    TEST_OFFSET(U16Vector1_GetValuePointer, 46);
    TEST_OFFSET(U16Vector1Array_GetValuePointer, 47);
    TEST_OFFSET(U16Vector1Array_GetLength, 48);

    TEST_OFFSET(I32Vector1_GetType, 49);
    TEST_OFFSET(I32Vector1Array_GetType, 50);
    TEST_OFFSET(I32Vector1_Create, 51);
    TEST_OFFSET(I32Vector1Array_Create, 52);
    TEST_OFFSET(I32Vector1_GetValuePointer, 53);
    TEST_OFFSET(I32Vector1Array_GetValuePointer, 54);
    TEST_OFFSET(I32Vector1Array_GetLength, 55);

    TEST_OFFSET(U32Vector1_GetType, 56);
    TEST_OFFSET(U32Vector1Array_GetType, 57);
    TEST_OFFSET(U32Vector1_Create, 58);
    TEST_OFFSET(U32Vector1Array_Create, 59);
    TEST_OFFSET(U32Vector1_GetValuePointer, 60);
    TEST_OFFSET(U32Vector1Array_GetValuePointer, 61);
    TEST_OFFSET(U32Vector1Array_GetLength, 62);

    TEST_OFFSET(IVector1_GetType, 63);
    TEST_OFFSET(IVector1Array_GetType, 64);
    TEST_OFFSET(IVector1_Create, 65);
    TEST_OFFSET(IVector1Array_Create, 66);
    TEST_OFFSET(IVector1_GetValuePointer, 67);
    TEST_OFFSET(IVector1Array_GetValuePointer, 68);
    TEST_OFFSET(IVector1Array_GetLength, 69);

    TEST_OFFSET(UVector1_GetType, 70);
    TEST_OFFSET(UVector1Array_GetType, 71);
    TEST_OFFSET(UVector1_Create, 72);
    TEST_OFFSET(UVector1Array_Create, 73);
    TEST_OFFSET(UVector1_GetValuePointer, 74);
    TEST_OFFSET(UVector1Array_GetValuePointer, 75);
    TEST_OFFSET(UVector1Array_GetLength, 76);

    TEST_OFFSET(I64Vector1_GetType, 77);
    TEST_OFFSET(I64Vector1Array_GetType, 78);
    TEST_OFFSET(I64Vector1_Create, 79);
    TEST_OFFSET(I64Vector1Array_Create, 80);
    TEST_OFFSET(I64Vector1_GetValuePointer, 81);
    TEST_OFFSET(I64Vector1Array_GetValuePointer, 82);
    TEST_OFFSET(I64Vector1Array_GetLength, 83);

    TEST_OFFSET(U64Vector1_GetType, 84);
    TEST_OFFSET(U64Vector1Array_GetType, 85);
    TEST_OFFSET(U64Vector1_Create, 86);
    TEST_OFFSET(U64Vector1Array_Create, 87);
    TEST_OFFSET(U64Vector1_GetValuePointer, 88);
    TEST_OFFSET(U64Vector1Array_GetValuePointer, 89);
    TEST_OFFSET(U64Vector1Array_GetLength, 90);

    TEST_OFFSET(BVector2_GetType, 91);
    TEST_OFFSET(BVector2Array_GetType, 92);
    TEST_OFFSET(BVector2_Create, 93);
    TEST_OFFSET(BVector2Array_Create, 94);
    TEST_OFFSET(BVector2_GetValuePointer, 95);
    TEST_OFFSET(BVector2Array_GetValuePointer, 96);
    TEST_OFFSET(BVector2Array_GetLength, 97);

    TEST_OFFSET(DVector2_GetType, 98);
    TEST_OFFSET(DVector2Array_GetType, 99);
    TEST_OFFSET(DVector2_Create, 100);
    TEST_OFFSET(DVector2Array_Create, 101);
    TEST_OFFSET(DVector2_GetValuePointer, 102);
    TEST_OFFSET(DVector2Array_GetValuePointer, 103);
    TEST_OFFSET(DVector2Array_GetLength, 104);

    TEST_OFFSET(FVector2_GetType, 105);
    TEST_OFFSET(FVector2Array_GetType, 106);
    TEST_OFFSET(FVector2_Create, 107);
    TEST_OFFSET(FVector2Array_Create, 108);
    TEST_OFFSET(FVector2_GetValuePointer, 109);
    TEST_OFFSET(FVector2Array_GetValuePointer, 110);
    TEST_OFFSET(FVector2Array_GetLength, 111);

    TEST_OFFSET(I8Vector2_GetType, 112);
    TEST_OFFSET(I8Vector2Array_GetType, 113);
    TEST_OFFSET(I8Vector2_Create, 114);
    TEST_OFFSET(I8Vector2Array_Create, 115);
    TEST_OFFSET(I8Vector2_GetValuePointer, 116);
    TEST_OFFSET(I8Vector2Array_GetValuePointer, 117);
    TEST_OFFSET(I8Vector2Array_GetLength, 118);

    TEST_OFFSET(U8Vector2_GetType, 119);
    TEST_OFFSET(U8Vector2Array_GetType, 120);
    TEST_OFFSET(U8Vector2_Create, 121);
    TEST_OFFSET(U8Vector2Array_Create, 122);
    TEST_OFFSET(U8Vector2_GetValuePointer, 123);
    TEST_OFFSET(U8Vector2Array_GetValuePointer, 124);
    TEST_OFFSET(U8Vector2Array_GetLength, 125);

    TEST_OFFSET(I16Vector2_GetType, 126);
    TEST_OFFSET(I16Vector2Array_GetType, 127);
    TEST_OFFSET(I16Vector2_Create, 128);
    TEST_OFFSET(I16Vector2Array_Create, 129);
    TEST_OFFSET(I16Vector2_GetValuePointer, 130);
    TEST_OFFSET(I16Vector2Array_GetValuePointer, 131);
    TEST_OFFSET(I16Vector2Array_GetLength, 132);

    TEST_OFFSET(U16Vector2_GetType, 133);
    TEST_OFFSET(U16Vector2Array_GetType, 134);
    TEST_OFFSET(U16Vector2_Create, 135);
    TEST_OFFSET(U16Vector2Array_Create, 136);
    TEST_OFFSET(U16Vector2_GetValuePointer, 137);
    TEST_OFFSET(U16Vector2Array_GetValuePointer, 138);
    TEST_OFFSET(U16Vector2Array_GetLength, 139);

    TEST_OFFSET(I32Vector2_GetType, 140);
    TEST_OFFSET(I32Vector2Array_GetType, 141);
    TEST_OFFSET(I32Vector2_Create, 142);
    TEST_OFFSET(I32Vector2Array_Create, 143);
    TEST_OFFSET(I32Vector2_GetValuePointer, 144);
    TEST_OFFSET(I32Vector2Array_GetValuePointer, 145);
    TEST_OFFSET(I32Vector2Array_GetLength, 146);

    TEST_OFFSET(U32Vector2_GetType, 147);
    TEST_OFFSET(U32Vector2Array_GetType, 148);
    TEST_OFFSET(U32Vector2_Create, 149);
    TEST_OFFSET(U32Vector2Array_Create, 150);
    TEST_OFFSET(U32Vector2_GetValuePointer, 151);
    TEST_OFFSET(U32Vector2Array_GetValuePointer, 152);
    TEST_OFFSET(U32Vector2Array_GetLength, 153);

    TEST_OFFSET(IVector2_GetType, 154);
    TEST_OFFSET(IVector2Array_GetType, 155);
    TEST_OFFSET(IVector2_Create, 156);
    TEST_OFFSET(IVector2Array_Create, 157);
    TEST_OFFSET(IVector2_GetValuePointer, 158);
    TEST_OFFSET(IVector2Array_GetValuePointer, 159);
    TEST_OFFSET(IVector2Array_GetLength, 160);

    TEST_OFFSET(UVector2_GetType, 161);
    TEST_OFFSET(UVector2Array_GetType, 162);
    TEST_OFFSET(UVector2_Create, 163);
    TEST_OFFSET(UVector2Array_Create, 164);
    TEST_OFFSET(UVector2_GetValuePointer, 165);
    TEST_OFFSET(UVector2Array_GetValuePointer, 166);
    TEST_OFFSET(UVector2Array_GetLength, 167);

    TEST_OFFSET(I64Vector2_GetType, 168);
    TEST_OFFSET(I64Vector2Array_GetType, 169);
    TEST_OFFSET(I64Vector2_Create, 170);
    TEST_OFFSET(I64Vector2Array_Create, 171);
    TEST_OFFSET(I64Vector2_GetValuePointer, 172);
    TEST_OFFSET(I64Vector2Array_GetValuePointer, 173);
    TEST_OFFSET(I64Vector2Array_GetLength, 174);

    TEST_OFFSET(U64Vector2_GetType, 175);
    TEST_OFFSET(U64Vector2Array_GetType, 176);
    TEST_OFFSET(U64Vector2_Create, 177);
    TEST_OFFSET(U64Vector2Array_Create, 178);
    TEST_OFFSET(U64Vector2_GetValuePointer, 179);
    TEST_OFFSET(U64Vector2Array_GetValuePointer, 180);
    TEST_OFFSET(U64Vector2Array_GetLength, 181);

    TEST_OFFSET(BVector3_GetType, 182);
    TEST_OFFSET(BVector3Array_GetType, 183);
    TEST_OFFSET(BVector3_Create, 184);
    TEST_OFFSET(BVector3Array_Create, 185);
    TEST_OFFSET(BVector3_GetValuePointer, 186);
    TEST_OFFSET(BVector3Array_GetValuePointer, 187);
    TEST_OFFSET(BVector3Array_GetLength, 188);

    TEST_OFFSET(DVector3_GetType, 189);
    TEST_OFFSET(DVector3Array_GetType, 190);
    TEST_OFFSET(DVector3_Create, 191);
    TEST_OFFSET(DVector3Array_Create, 192);
    TEST_OFFSET(DVector3_GetValuePointer, 193);
    TEST_OFFSET(DVector3Array_GetValuePointer, 194);
    TEST_OFFSET(DVector3Array_GetLength, 195);

    TEST_OFFSET(FVector3_GetType, 196);
    TEST_OFFSET(FVector3Array_GetType, 197);
    TEST_OFFSET(FVector3_Create, 198);
    TEST_OFFSET(FVector3Array_Create, 199);
    TEST_OFFSET(FVector3_GetValuePointer, 200);
    TEST_OFFSET(FVector3Array_GetValuePointer, 201);
    TEST_OFFSET(FVector3Array_GetLength, 202);

    TEST_OFFSET(I8Vector3_GetType, 203);
    TEST_OFFSET(I8Vector3Array_GetType, 204);
    TEST_OFFSET(I8Vector3_Create, 205);
    TEST_OFFSET(I8Vector3Array_Create, 206);
    TEST_OFFSET(I8Vector3_GetValuePointer, 207);
    TEST_OFFSET(I8Vector3Array_GetValuePointer, 208);
    TEST_OFFSET(I8Vector3Array_GetLength, 209);

    TEST_OFFSET(U8Vector3_GetType, 210);
    TEST_OFFSET(U8Vector3Array_GetType, 211);
    TEST_OFFSET(U8Vector3_Create, 212);
    TEST_OFFSET(U8Vector3Array_Create, 213);
    TEST_OFFSET(U8Vector3_GetValuePointer, 214);
    TEST_OFFSET(U8Vector3Array_GetValuePointer, 215);
    TEST_OFFSET(U8Vector3Array_GetLength, 216);

    TEST_OFFSET(I16Vector3_GetType, 217);
    TEST_OFFSET(I16Vector3Array_GetType, 218);
    TEST_OFFSET(I16Vector3_Create, 219);
    TEST_OFFSET(I16Vector3Array_Create, 220);
    TEST_OFFSET(I16Vector3_GetValuePointer, 221);
    TEST_OFFSET(I16Vector3Array_GetValuePointer, 222);
    TEST_OFFSET(I16Vector3Array_GetLength, 223);

    TEST_OFFSET(U16Vector3_GetType, 224);
    TEST_OFFSET(U16Vector3Array_GetType, 225);
    TEST_OFFSET(U16Vector3_Create, 226);
    TEST_OFFSET(U16Vector3Array_Create, 227);
    TEST_OFFSET(U16Vector3_GetValuePointer, 228);
    TEST_OFFSET(U16Vector3Array_GetValuePointer, 229);
    TEST_OFFSET(U16Vector3Array_GetLength, 230);

    TEST_OFFSET(I32Vector3_GetType, 231);
    TEST_OFFSET(I32Vector3Array_GetType, 232);
    TEST_OFFSET(I32Vector3_Create, 233);
    TEST_OFFSET(I32Vector3Array_Create, 234);
    TEST_OFFSET(I32Vector3_GetValuePointer, 235);
    TEST_OFFSET(I32Vector3Array_GetValuePointer, 236);
    TEST_OFFSET(I32Vector3Array_GetLength, 237);

    TEST_OFFSET(U32Vector3_GetType, 238);
    TEST_OFFSET(U32Vector3Array_GetType, 239);
    TEST_OFFSET(U32Vector3_Create, 240);
    TEST_OFFSET(U32Vector3Array_Create, 241);
    TEST_OFFSET(U32Vector3_GetValuePointer, 242);
    TEST_OFFSET(U32Vector3Array_GetValuePointer, 243);
    TEST_OFFSET(U32Vector3Array_GetLength, 244);

    TEST_OFFSET(IVector3_GetType, 245);
    TEST_OFFSET(IVector3Array_GetType, 246);
    TEST_OFFSET(IVector3_Create, 247);
    TEST_OFFSET(IVector3Array_Create, 248);
    TEST_OFFSET(IVector3_GetValuePointer, 249);
    TEST_OFFSET(IVector3Array_GetValuePointer, 250);
    TEST_OFFSET(IVector3Array_GetLength, 251);

    TEST_OFFSET(UVector3_GetType, 252);
    TEST_OFFSET(UVector3Array_GetType, 253);
    TEST_OFFSET(UVector3_Create, 254);
    TEST_OFFSET(UVector3Array_Create, 255);
    TEST_OFFSET(UVector3_GetValuePointer, 256);
    TEST_OFFSET(UVector3Array_GetValuePointer, 257);
    TEST_OFFSET(UVector3Array_GetLength, 258);

    TEST_OFFSET(I64Vector3_GetType, 259);
    TEST_OFFSET(I64Vector3Array_GetType, 260);
    TEST_OFFSET(I64Vector3_Create, 261);
    TEST_OFFSET(I64Vector3Array_Create, 262);
    TEST_OFFSET(I64Vector3_GetValuePointer, 263);
    TEST_OFFSET(I64Vector3Array_GetValuePointer, 264);
    TEST_OFFSET(I64Vector3Array_GetLength, 265);

    TEST_OFFSET(U64Vector3_GetType, 266);
    TEST_OFFSET(U64Vector3Array_GetType, 267);
    TEST_OFFSET(U64Vector3_Create, 268);
    TEST_OFFSET(U64Vector3Array_Create, 269);
    TEST_OFFSET(U64Vector3_GetValuePointer, 270);
    TEST_OFFSET(U64Vector3Array_GetValuePointer, 271);
    TEST_OFFSET(U64Vector3Array_GetLength, 272);

    TEST_OFFSET(BVector4_GetType, 273);
    TEST_OFFSET(BVector4Array_GetType, 274);
    TEST_OFFSET(BVector4_Create, 275);
    TEST_OFFSET(BVector4Array_Create, 276);
    TEST_OFFSET(BVector4_GetValuePointer, 277);
    TEST_OFFSET(BVector4Array_GetValuePointer, 278);
    TEST_OFFSET(BVector4Array_GetLength, 279);

    TEST_OFFSET(DVector4_GetType, 280);
    TEST_OFFSET(DVector4Array_GetType, 281);
    TEST_OFFSET(DVector4_Create, 282);
    TEST_OFFSET(DVector4Array_Create, 283);
    TEST_OFFSET(DVector4_GetValuePointer, 284);
    TEST_OFFSET(DVector4Array_GetValuePointer, 285);
    TEST_OFFSET(DVector4Array_GetLength, 286);

    TEST_OFFSET(FVector4_GetType, 287);
    TEST_OFFSET(FVector4Array_GetType, 288);
    TEST_OFFSET(FVector4_Create, 289);
    TEST_OFFSET(FVector4Array_Create, 290);
    TEST_OFFSET(FVector4_GetValuePointer, 291);
    TEST_OFFSET(FVector4Array_GetValuePointer, 292);
    TEST_OFFSET(FVector4Array_GetLength, 293);

    TEST_OFFSET(I8Vector4_GetType, 294);
    TEST_OFFSET(I8Vector4Array_GetType, 295);
    TEST_OFFSET(I8Vector4_Create, 296);
    TEST_OFFSET(I8Vector4Array_Create, 297);
    TEST_OFFSET(I8Vector4_GetValuePointer, 298);
    TEST_OFFSET(I8Vector4Array_GetValuePointer, 299);
    TEST_OFFSET(I8Vector4Array_GetLength, 300);

    TEST_OFFSET(U8Vector4_GetType, 301);
    TEST_OFFSET(U8Vector4Array_GetType, 302);
    TEST_OFFSET(U8Vector4_Create, 303);
    TEST_OFFSET(U8Vector4Array_Create, 304);
    TEST_OFFSET(U8Vector4_GetValuePointer, 305);
    TEST_OFFSET(U8Vector4Array_GetValuePointer, 306);
    TEST_OFFSET(U8Vector4Array_GetLength, 307);

    TEST_OFFSET(I16Vector4_GetType, 308);
    TEST_OFFSET(I16Vector4Array_GetType, 309);
    TEST_OFFSET(I16Vector4_Create, 310);
    TEST_OFFSET(I16Vector4Array_Create, 311);
    TEST_OFFSET(I16Vector4_GetValuePointer, 312);
    TEST_OFFSET(I16Vector4Array_GetValuePointer, 313);
    TEST_OFFSET(I16Vector4Array_GetLength, 314);

    TEST_OFFSET(U16Vector4_GetType, 315);
    TEST_OFFSET(U16Vector4Array_GetType, 316);
    TEST_OFFSET(U16Vector4_Create, 317);
    TEST_OFFSET(U16Vector4Array_Create, 318);
    TEST_OFFSET(U16Vector4_GetValuePointer, 319);
    TEST_OFFSET(U16Vector4Array_GetValuePointer, 320);
    TEST_OFFSET(U16Vector4Array_GetLength, 321);

    TEST_OFFSET(I32Vector4_GetType, 322);
    TEST_OFFSET(I32Vector4Array_GetType, 323);
    TEST_OFFSET(I32Vector4_Create, 324);
    TEST_OFFSET(I32Vector4Array_Create, 325);
    TEST_OFFSET(I32Vector4_GetValuePointer, 326);
    TEST_OFFSET(I32Vector4Array_GetValuePointer, 327);
    TEST_OFFSET(I32Vector4Array_GetLength, 328);

    TEST_OFFSET(U32Vector4_GetType, 329);
    TEST_OFFSET(U32Vector4Array_GetType, 330);
    TEST_OFFSET(U32Vector4_Create, 331);
    TEST_OFFSET(U32Vector4Array_Create, 332);
    TEST_OFFSET(U32Vector4_GetValuePointer, 333);
    TEST_OFFSET(U32Vector4Array_GetValuePointer, 334);
    TEST_OFFSET(U32Vector4Array_GetLength, 335);

    TEST_OFFSET(IVector4_GetType, 336);
    TEST_OFFSET(IVector4Array_GetType, 337);
    TEST_OFFSET(IVector4_Create, 338);
    TEST_OFFSET(IVector4Array_Create, 339);
    TEST_OFFSET(IVector4_GetValuePointer, 340);
    TEST_OFFSET(IVector4Array_GetValuePointer, 341);
    TEST_OFFSET(IVector4Array_GetLength, 342);

    TEST_OFFSET(UVector4_GetType, 343);
    TEST_OFFSET(UVector4Array_GetType, 344);
    TEST_OFFSET(UVector4_Create, 345);
    TEST_OFFSET(UVector4Array_Create, 346);
    TEST_OFFSET(UVector4_GetValuePointer, 347);
    TEST_OFFSET(UVector4Array_GetValuePointer, 348);
    TEST_OFFSET(UVector4Array_GetLength, 349);

    TEST_OFFSET(I64Vector4_GetType, 350);
    TEST_OFFSET(I64Vector4Array_GetType, 351);
    TEST_OFFSET(I64Vector4_Create, 352);
    TEST_OFFSET(I64Vector4Array_Create, 353);
    TEST_OFFSET(I64Vector4_GetValuePointer, 354);
    TEST_OFFSET(I64Vector4Array_GetValuePointer, 355);
    TEST_OFFSET(I64Vector4Array_GetLength, 356);

    TEST_OFFSET(U64Vector4_GetType, 357);
    TEST_OFFSET(U64Vector4Array_GetType, 358);
    TEST_OFFSET(U64Vector4_Create, 359);
    TEST_OFFSET(U64Vector4Array_Create, 360);
    TEST_OFFSET(U64Vector4_GetValuePointer, 361);
    TEST_OFFSET(U64Vector4Array_GetValuePointer, 362);
    TEST_OFFSET(U64Vector4Array_GetLength, 363);

    TEST_OFFSET(DMatrix2x2_GetType, 364);
    TEST_OFFSET(DMatrix2x2Array_GetType, 365);
    TEST_OFFSET(DMatrix2x2_Create, 366);
    TEST_OFFSET(DMatrix2x2Array_Create, 367);
    TEST_OFFSET(DMatrix2x2_GetValuePointer, 368);
    TEST_OFFSET(DMatrix2x2Array_GetValuePointer, 369);
    TEST_OFFSET(DMatrix2x2Array_GetLength, 370);

    TEST_OFFSET(FMatrix2x2_GetType, 371);
    TEST_OFFSET(FMatrix2x2Array_GetType, 372);
    TEST_OFFSET(FMatrix2x2_Create, 373);
    TEST_OFFSET(FMatrix2x2Array_Create, 374);
    TEST_OFFSET(FMatrix2x2_GetValuePointer, 375);
    TEST_OFFSET(FMatrix2x2Array_GetValuePointer, 376);
    TEST_OFFSET(FMatrix2x2Array_GetLength, 377);

    TEST_OFFSET(DMatrix2x3_GetType, 378);
    TEST_OFFSET(DMatrix2x3Array_GetType, 379);
    TEST_OFFSET(DMatrix2x3_Create, 380);
    TEST_OFFSET(DMatrix2x3Array_Create, 381);
    TEST_OFFSET(DMatrix2x3_GetValuePointer, 382);
    TEST_OFFSET(DMatrix2x3Array_GetValuePointer, 383);
    TEST_OFFSET(DMatrix2x3Array_GetLength, 384);

    TEST_OFFSET(FMatrix2x3_GetType, 385);
    TEST_OFFSET(FMatrix2x3Array_GetType, 386);
    TEST_OFFSET(FMatrix2x3_Create, 387);
    TEST_OFFSET(FMatrix2x3Array_Create, 388);
    TEST_OFFSET(FMatrix2x3_GetValuePointer, 389);
    TEST_OFFSET(FMatrix2x3Array_GetValuePointer, 390);
    TEST_OFFSET(FMatrix2x3Array_GetLength, 391);

    TEST_OFFSET(DMatrix2x4_GetType, 392);
    TEST_OFFSET(DMatrix2x4Array_GetType, 393);
    TEST_OFFSET(DMatrix2x4_Create, 394);
    TEST_OFFSET(DMatrix2x4Array_Create, 395);
    TEST_OFFSET(DMatrix2x4_GetValuePointer, 396);
    TEST_OFFSET(DMatrix2x4Array_GetValuePointer, 397);
    TEST_OFFSET(DMatrix2x4Array_GetLength, 398);

    TEST_OFFSET(FMatrix2x4_GetType, 399);
    TEST_OFFSET(FMatrix2x4Array_GetType, 400);
    TEST_OFFSET(FMatrix2x4_Create, 401);
    TEST_OFFSET(FMatrix2x4Array_Create, 402);
    TEST_OFFSET(FMatrix2x4_GetValuePointer, 403);
    TEST_OFFSET(FMatrix2x4Array_GetValuePointer, 404);
    TEST_OFFSET(FMatrix2x4Array_GetLength, 405);

    TEST_OFFSET(DMatrix3x2_GetType, 406);
    TEST_OFFSET(DMatrix3x2Array_GetType, 407);
    TEST_OFFSET(DMatrix3x2_Create, 408);
    TEST_OFFSET(DMatrix3x2Array_Create, 409);
    TEST_OFFSET(DMatrix3x2_GetValuePointer, 410);
    TEST_OFFSET(DMatrix3x2Array_GetValuePointer, 411);
    TEST_OFFSET(DMatrix3x2Array_GetLength, 412);

    TEST_OFFSET(FMatrix3x2_GetType, 413);
    TEST_OFFSET(FMatrix3x2Array_GetType, 414);
    TEST_OFFSET(FMatrix3x2_Create, 415);
    TEST_OFFSET(FMatrix3x2Array_Create, 416);
    TEST_OFFSET(FMatrix3x2_GetValuePointer, 417);
    TEST_OFFSET(FMatrix3x2Array_GetValuePointer, 418);
    TEST_OFFSET(FMatrix3x2Array_GetLength, 419);

    TEST_OFFSET(DMatrix3x3_GetType, 420);
    TEST_OFFSET(DMatrix3x3Array_GetType, 421);
    TEST_OFFSET(DMatrix3x3_Create, 422);
    TEST_OFFSET(DMatrix3x3Array_Create, 423);
    TEST_OFFSET(DMatrix3x3_GetValuePointer, 424);
    TEST_OFFSET(DMatrix3x3Array_GetValuePointer, 425);
    TEST_OFFSET(DMatrix3x3Array_GetLength, 426);

    TEST_OFFSET(FMatrix3x3_GetType, 427);
    TEST_OFFSET(FMatrix3x3Array_GetType, 428);
    TEST_OFFSET(FMatrix3x3_Create, 429);
    TEST_OFFSET(FMatrix3x3Array_Create, 430);
    TEST_OFFSET(FMatrix3x3_GetValuePointer, 431);
    TEST_OFFSET(FMatrix3x3Array_GetValuePointer, 432);
    TEST_OFFSET(FMatrix3x3Array_GetLength, 433);

    TEST_OFFSET(DMatrix3x4_GetType, 434);
    TEST_OFFSET(DMatrix3x4Array_GetType, 435);
    TEST_OFFSET(DMatrix3x4_Create, 436);
    TEST_OFFSET(DMatrix3x4Array_Create, 437);
    TEST_OFFSET(DMatrix3x4_GetValuePointer, 438);
    TEST_OFFSET(DMatrix3x4Array_GetValuePointer, 439);
    TEST_OFFSET(DMatrix3x4Array_GetLength, 440);

    TEST_OFFSET(FMatrix3x4_GetType, 441);
    TEST_OFFSET(FMatrix3x4Array_GetType, 442);
    TEST_OFFSET(FMatrix3x4_Create, 443);
    TEST_OFFSET(FMatrix3x4Array_Create, 444);
    TEST_OFFSET(FMatrix3x4_GetValuePointer, 445);
    TEST_OFFSET(FMatrix3x4Array_GetValuePointer, 446);
    TEST_OFFSET(FMatrix3x4Array_GetLength, 447);

    TEST_OFFSET(DMatrix4x2_GetType, 448);
    TEST_OFFSET(DMatrix4x2Array_GetType, 449);
    TEST_OFFSET(DMatrix4x2_Create, 450);
    TEST_OFFSET(DMatrix4x2Array_Create, 451);
    TEST_OFFSET(DMatrix4x2_GetValuePointer, 452);
    TEST_OFFSET(DMatrix4x2Array_GetValuePointer, 453);
    TEST_OFFSET(DMatrix4x2Array_GetLength, 454);

    TEST_OFFSET(FMatrix4x2_GetType, 455);
    TEST_OFFSET(FMatrix4x2Array_GetType, 456);
    TEST_OFFSET(FMatrix4x2_Create, 457);
    TEST_OFFSET(FMatrix4x2Array_Create, 458);
    TEST_OFFSET(FMatrix4x2_GetValuePointer, 459);
    TEST_OFFSET(FMatrix4x2Array_GetValuePointer, 460);
    TEST_OFFSET(FMatrix4x2Array_GetLength, 461);

    TEST_OFFSET(DMatrix4x3_GetType, 462);
    TEST_OFFSET(DMatrix4x3Array_GetType, 463);
    TEST_OFFSET(DMatrix4x3_Create, 464);
    TEST_OFFSET(DMatrix4x3Array_Create, 465);
    TEST_OFFSET(DMatrix4x3_GetValuePointer, 466);
    TEST_OFFSET(DMatrix4x3Array_GetValuePointer, 467);
    TEST_OFFSET(DMatrix4x3Array_GetLength, 468);

    TEST_OFFSET(FMatrix4x3_GetType, 469);
    TEST_OFFSET(FMatrix4x3Array_GetType, 470);
    TEST_OFFSET(FMatrix4x3_Create, 471);
    TEST_OFFSET(FMatrix4x3Array_Create, 472);
    TEST_OFFSET(FMatrix4x3_GetValuePointer, 473);
    TEST_OFFSET(FMatrix4x3Array_GetValuePointer, 474);
    TEST_OFFSET(FMatrix4x3Array_GetLength, 475);

    TEST_OFFSET(DMatrix4x4_GetType, 476);
    TEST_OFFSET(DMatrix4x4Array_GetType, 477);
    TEST_OFFSET(DMatrix4x4_Create, 478);
    TEST_OFFSET(DMatrix4x4Array_Create, 479);
    TEST_OFFSET(DMatrix4x4_GetValuePointer, 480);
    TEST_OFFSET(DMatrix4x4Array_GetValuePointer, 481);
    TEST_OFFSET(DMatrix4x4Array_GetLength, 482);

    TEST_OFFSET(FMatrix4x4_GetType, 483);
    TEST_OFFSET(FMatrix4x4Array_GetType, 484);
    TEST_OFFSET(FMatrix4x4_Create, 485);
    TEST_OFFSET(FMatrix4x4Array_Create, 486);
    TEST_OFFSET(FMatrix4x4_GetValuePointer, 487);
    TEST_OFFSET(FMatrix4x4Array_GetValuePointer, 488);
    TEST_OFFSET(FMatrix4x4Array_GetLength, 489);

    TEST_OFFSET(DQuaternion_GetType, 490);
    TEST_OFFSET(DQuaternionArray_GetType, 491);
    TEST_OFFSET(DQuaternion_Create, 492);
    TEST_OFFSET(DQuaternionArray_Create, 493);
    TEST_OFFSET(DQuaternion_GetValuePointer, 494);
    TEST_OFFSET(DQuaternionArray_GetValuePointer, 495);
    TEST_OFFSET(DQuaternionArray_GetLength, 496);

    TEST_OFFSET(FQuaternion_GetType, 497);
    TEST_OFFSET(FQuaternionArray_GetType, 498);
    TEST_OFFSET(FQuaternion_Create, 499);
    TEST_OFFSET(FQuaternionArray_Create, 500);
    TEST_OFFSET(FQuaternion_GetValuePointer, 501);
    TEST_OFFSET(FQuaternionArray_GetValuePointer, 502);
    TEST_OFFSET(FQuaternionArray_GetLength, 503);

    TEST_OFFSET(BArray_GetType, 504);
    TEST_OFFSET(BArray_Create, 505);
    TEST_OFFSET(BArray_GetValuePointer, 506);
    TEST_OFFSET(BArray_GetLength, 507);

    TEST_OFFSET(DArray_GetType, 508);
    TEST_OFFSET(DArray_Create, 509);
    TEST_OFFSET(DArray_GetValuePointer, 510);
    TEST_OFFSET(DArray_GetLength, 511);

    TEST_OFFSET(FArray_GetType, 512);
    TEST_OFFSET(FArray_Create, 513);
    TEST_OFFSET(FArray_GetValuePointer, 514);
    TEST_OFFSET(FArray_GetLength, 515);

    TEST_OFFSET(I8Array_GetType, 516);
    TEST_OFFSET(I8Array_Create, 517);
    TEST_OFFSET(I8Array_GetValuePointer, 518);
    TEST_OFFSET(I8Array_GetLength, 519);

    TEST_OFFSET(U8Array_GetType, 520);
    TEST_OFFSET(U8Array_Create, 521);
    TEST_OFFSET(U8Array_GetValuePointer, 522);
    TEST_OFFSET(U8Array_GetLength, 523);

    TEST_OFFSET(I16Array_GetType, 524);
    TEST_OFFSET(I16Array_Create, 525);
    TEST_OFFSET(I16Array_GetValuePointer, 526);
    TEST_OFFSET(I16Array_GetLength, 527);

    TEST_OFFSET(U16Array_GetType, 528);
    TEST_OFFSET(U16Array_Create, 529);
    TEST_OFFSET(U16Array_GetValuePointer, 530);
    TEST_OFFSET(U16Array_GetLength, 531);

    TEST_OFFSET(I32Array_GetType, 532);
    TEST_OFFSET(I32Array_Create, 533);
    TEST_OFFSET(I32Array_GetValuePointer, 534);
    TEST_OFFSET(I32Array_GetLength, 535);

    TEST_OFFSET(U32Array_GetType, 536);
    TEST_OFFSET(U32Array_Create, 537);
    TEST_OFFSET(U32Array_GetValuePointer, 538);
    TEST_OFFSET(U32Array_GetLength, 539);

    TEST_OFFSET(IArray_GetType, 540);
    TEST_OFFSET(IArray_Create, 541);
    TEST_OFFSET(IArray_GetValuePointer, 542);
    TEST_OFFSET(IArray_GetLength, 543);

    TEST_OFFSET(UArray_GetType, 544);
    TEST_OFFSET(UArray_Create, 545);
    TEST_OFFSET(UArray_GetValuePointer, 546);
    TEST_OFFSET(UArray_GetLength, 547);

    TEST_OFFSET(I64Array_GetType, 548);
    TEST_OFFSET(I64Array_Create, 549);
    TEST_OFFSET(I64Array_GetValuePointer, 550);
    TEST_OFFSET(I64Array_GetLength, 551);

    TEST_OFFSET(U64Array_GetType, 552);
    TEST_OFFSET(U64Array_Create, 553);
    TEST_OFFSET(U64Array_GetValuePointer, 554);
    TEST_OFFSET(U64Array_GetLength, 555);

    {% for type in vector_types + matrix_types + quaternion_types + pod_types %}
        {% if type not in pod_types %}
            TEST(api->{{ type }}_GetType != 0);
            TEST(api->{{ type }}_Create != 0);
            TEST(api->{{ type }}_GetValuePointer != 0);
        {% endif %}
        TEST(api->{{ type }}Array_Create != 0);
        TEST(api->{{ type }}Array_GetType != 0);
        TEST(api->{{ type }}Array_GetValuePointer != 0);
        TEST(api->{{ type }}Array_GetLength != 0);
    {% endfor %}

    EMathApi_Release();
    TEST(!PyErr_Occurred());

    Py_RETURN_NONE;
}


{% for type in vector_types %}
{% with component_count=int(type[-1]) %}
{% with c_type={
    "B": 'bool',
    "F": 'float',
    "D": 'double',
    "I": 'int',
    "I8": 'int8_t',
    "I16": 'int16_t',
    "I32": 'int32_t',
    "I64": 'int64_t',
    "U": 'unsigned int',
    "U8": 'uint8_t',
    "U16": 'uint16_t',
    "U32": 'uint32_t',
    "U64": 'uint64_t',
}[type[:type.find('V')]] %}
    static PyObject *
    test_{{ type }}(PyObject *self, PyObject *args)
    {
        struct EMathApi *api = EMathApi_Get();
        if (!api){ return 0; }
        TEST(!PyErr_Occurred());

        PyTypeObject *type = api->{{ type }}_GetType();
        TEST(type != 0);
        TEST(!PyErr_Occurred());

        {
            {{ c_type }} components[{{ component_count }}] = {
                {% for i in range(component_count) %}
                    {{ i }}{% if i != component_count - 1 %}, {% endif %}
                {% endfor %}
            };
            PyObject *obj = api->{{ type }}_Create(components);
            TEST(obj != 0);
            TEST(!PyErr_Occurred());
            TEST(Py_TYPE(obj) == type);

            const {{ c_type }} *value_ptr = api->{{ type }}_GetValuePointer(obj);
            TEST(value_ptr != 0);
            TEST(!PyErr_Occurred());
            {% for i in range(component_count) %}
                TEST(value_ptr[{{ i }}] == ({{ c_type }}){{ i }});
            {% endfor %}

            Py_DECREF(obj);
        }

        Py_INCREF(Py_None);
        const {{ c_type }} *value_ptr = api->{{ type }}_GetValuePointer(Py_None);
        TEST(value_ptr == 0);
        TEST(PyErr_Occurred());
        PyErr_Clear();
        Py_DECREF(Py_None);

        EMathApi_Release();
        TEST(!PyErr_Occurred());

        Py_RETURN_NONE;
    }

    static PyObject *
    test_{{ type }}Array(PyObject *self, PyObject *args)
    {
        struct EMathApi *api = EMathApi_Get();
        if (!api){ return 0; }
        TEST(!PyErr_Occurred());

        PyTypeObject *type = api->{{ type }}Array_GetType();
        TEST(type != 0);
        TEST(!PyErr_Occurred());

        {{ c_type }} components[{{ component_count * 10 }}] = {
            {% for i in range(component_count * 10) %}
                {{ i }}{% if i != (component_count * 10) - 1 %}, {% endif %}
            {% endfor %}
        };
        for (size_t i = 0; i < 10; i++)
        {
            PyObject *obj = api->{{ type }}Array_Create(i, components);
            TEST(obj != 0);
            TEST(!PyErr_Occurred());
            TEST(Py_TYPE(obj) == type);

            size_t length = api->{{ type }}Array_GetLength(obj);
            TEST(length == i);
            TEST(!PyErr_Occurred());

            const {{ c_type }} *value_ptr = api->{{ type }}Array_GetValuePointer(obj);
            if (i == 0)
            {
                TEST(value_ptr == 0);
            }
            else
            {
                TEST(value_ptr != 0);
            }
            TEST(!PyErr_Occurred());
            for (size_t j = 0; j < i * {{ component_count }}; j++)
            {
                TEST(value_ptr[j] == ({{ c_type }})j);
            }

            Py_DECREF(obj);
        }

        Py_INCREF(Py_None);
        size_t length = api->{{ type }}Array_GetLength(Py_None);
        TEST(length == 0);
        TEST(PyErr_Occurred());
        PyErr_Clear();
        const {{ c_type }} *value_ptr = api->{{ type }}Array_GetValuePointer(Py_None);
        TEST(value_ptr == 0);
        TEST(PyErr_Occurred());
        PyErr_Clear();
        Py_DECREF(Py_None);

        EMathApi_Release();
        TEST(!PyErr_Occurred());

        Py_RETURN_NONE;
    }
{% endwith %}
{% endwith %}
{% endfor %}


{% for type in matrix_types %}
{% with row_size=int(type[-3]) %}
{% with column_size=int(type[-1]) %}
{% with component_count=row_size * column_size %}
{% with c_type={
    "F": 'float',
    "D": 'double',
}[type[:type.find('M')]] %}
    static PyObject *
    test_{{ type }}(PyObject *self, PyObject *args)
    {
        struct EMathApi *api = EMathApi_Get();
        if (!api){ return 0; }
        TEST(!PyErr_Occurred());

        PyTypeObject *type = api->{{ type }}_GetType();
        TEST(type != 0);
        TEST(!PyErr_Occurred());

        {
            {{ c_type }} components[{{ component_count }}] = {
                {% for i in range(component_count) %}
                    {{ i }}{% if i != component_count - 1 %}, {% endif %}
                {% endfor %}
            };
            PyObject *obj = api->{{ type }}_Create(components);
            TEST(obj != 0);
            TEST(!PyErr_Occurred());
            TEST(Py_TYPE(obj) == type);

            {{ c_type }} *value_ptr = api->{{ type }}_GetValuePointer(obj);
            TEST(value_ptr != 0);
            TEST(!PyErr_Occurred());
            {% for i in range(component_count) %}
                TEST(value_ptr[{{ i }}] == ({{ c_type }}){{ i }});
            {% endfor %}

            Py_DECREF(obj);
        }

        Py_INCREF(Py_None);
        {{ c_type }} *value_ptr = api->{{ type }}_GetValuePointer(Py_None);
        TEST(value_ptr == 0);
        TEST(PyErr_Occurred());
        PyErr_Clear();
        Py_DECREF(Py_None);

        EMathApi_Release();
        TEST(!PyErr_Occurred());

        Py_RETURN_NONE;
    }

    static PyObject *
    test_{{ type }}Array(PyObject *self, PyObject *args)
    {
        struct EMathApi *api = EMathApi_Get();
        if (!api){ return 0; }
        TEST(!PyErr_Occurred());

        PyTypeObject *type = api->{{ type }}Array_GetType();
        TEST(type != 0);
        TEST(!PyErr_Occurred());

        {{ c_type }} components[{{ component_count * 10 }}] = {
            {% for i in range(component_count * 10) %}
                {{ i }}{% if i != (component_count * 10) - 1 %}, {% endif %}
            {% endfor %}
        };
        for (size_t i = 0; i < 10; i++)
        {
            PyObject *obj = api->{{ type }}Array_Create(i, components);
            TEST(obj != 0);
            TEST(!PyErr_Occurred());
            TEST(Py_TYPE(obj) == type);

            size_t length = api->{{ type }}Array_GetLength(obj);
            TEST(length == i);
            TEST(!PyErr_Occurred());

            {{ c_type }} *value_ptr = api->{{ type }}Array_GetValuePointer(obj);
            if (i == 0)
            {
                TEST(value_ptr == 0);
            }
            else
            {
                TEST(value_ptr != 0);
            }
            TEST(!PyErr_Occurred());
            for (size_t j = 0; j < i * {{ component_count }}; j++)
            {
                TEST(value_ptr[j] == ({{ c_type }})j);
            }

            Py_DECREF(obj);
        }

        Py_INCREF(Py_None);
        size_t length = api->{{ type }}Array_GetLength(Py_None);
        TEST(length == 0);
        TEST(PyErr_Occurred());
        PyErr_Clear();
        {{ c_type }} *value_ptr = api->{{ type }}Array_GetValuePointer(Py_None);
        TEST(value_ptr == 0);
        TEST(PyErr_Occurred());
        PyErr_Clear();
        Py_DECREF(Py_None);

        EMathApi_Release();
        TEST(!PyErr_Occurred());

        Py_RETURN_NONE;
    }
{% endwith %}
{% endwith %}
{% endwith %}
{% endwith %}
{% endfor %}


{% for type in quaternion_types %}
{% with c_type={
    "F": 'float',
    "D": 'double',
}[type[:type.find('Q')]] %}
    static PyObject *
    test_{{ type }}(PyObject *self, PyObject *args)
    {
        struct EMathApi *api = EMathApi_Get();
        if (!api){ return 0; }
        TEST(!PyErr_Occurred());

        PyTypeObject *type = api->{{ type }}_GetType();
        TEST(type != 0);
        TEST(!PyErr_Occurred());

        {
            {{ c_type }} components[4] = {
                {% for i in range(4) %}
                    {{ i }}{% if i != 3 %}, {% endif %}
                {% endfor %}
            };
            PyObject *obj = api->{{ type }}_Create(components);
            TEST(obj != 0);
            TEST(!PyErr_Occurred());
            TEST(Py_TYPE(obj) == type);

            {{ c_type }} *value_ptr = api->{{ type }}_GetValuePointer(obj);
            TEST(value_ptr != 0);
            TEST(!PyErr_Occurred());
            {% for i in range(4) %}
                TEST(value_ptr[{{ i }}] == ({{ c_type }}){{ i }});
            {% endfor %}

            Py_DECREF(obj);
        }

        Py_INCREF(Py_None);
        {{ c_type }} *value_ptr = api->{{ type }}_GetValuePointer(Py_None);
        TEST(value_ptr == 0);
        TEST(PyErr_Occurred());
        PyErr_Clear();
        Py_DECREF(Py_None);

        EMathApi_Release();
        TEST(!PyErr_Occurred());

        Py_RETURN_NONE;
    }

    static PyObject *
    test_{{ type }}Array(PyObject *self, PyObject *args)
    {
        struct EMathApi *api = EMathApi_Get();
        if (!api){ return 0; }
        TEST(!PyErr_Occurred());

        PyTypeObject *type = api->{{ type }}Array_GetType();
        TEST(type != 0);
        TEST(!PyErr_Occurred());

        {{ c_type }} components[{{ 4 * 10 }}] = {
            {% for i in range(4 * 10) %}
                {{ i }}{% if i != (4 * 10) - 1 %}, {% endif %}
            {% endfor %}
        };
        for (size_t i = 0; i < 10; i++)
        {
            PyObject *obj = api->{{ type }}Array_Create(i, components);
            TEST(obj != 0);
            TEST(!PyErr_Occurred());
            TEST(Py_TYPE(obj) == type);

            size_t length = api->{{ type }}Array_GetLength(obj);
            TEST(length == i);
            TEST(!PyErr_Occurred());

            {{ c_type }} *value_ptr = api->{{ type }}Array_GetValuePointer(obj);
            if (i == 0)
            {
                TEST(value_ptr == 0);
            }
            else
            {
                TEST(value_ptr != 0);
            }
            TEST(!PyErr_Occurred());
            for (size_t j = 0; j < i * {{ 4 }}; j++)
            {
                TEST(value_ptr[j] == ({{ c_type }})j);
            }

            Py_DECREF(obj);
        }

        Py_INCREF(Py_None);
        size_t length = api->{{ type }}Array_GetLength(Py_None);
        TEST(length == 0);
        TEST(PyErr_Occurred());
        PyErr_Clear();
        {{ c_type }} *value_ptr = api->{{ type }}Array_GetValuePointer(Py_None);
        TEST(value_ptr == 0);
        TEST(PyErr_Occurred());
        PyErr_Clear();
        Py_DECREF(Py_None);

        EMathApi_Release();
        TEST(!PyErr_Occurred());

        Py_RETURN_NONE;
    }
{% endwith %}
{% endfor %}


{% for type in pod_types %}
{% with c_type={
    "B": 'bool',
    "F": 'float',
    "D": 'double',
    "I": 'int',
    "I8": 'int8_t',
    "I16": 'int16_t',
    "I32": 'int32_t',
    "I64": 'int64_t',
    "U": 'unsigned int',
    "U8": 'uint8_t',
    "U16": 'uint16_t',
    "U32": 'uint32_t',
    "U64": 'uint64_t',
}[type] %}
    static PyObject *
    test_{{ type }}Array(PyObject *self, PyObject *args)
    {
        struct EMathApi *api = EMathApi_Get();
        if (!api){ return 0; }
        TEST(!PyErr_Occurred());

        PyTypeObject *type = api->{{ type }}Array_GetType();
        TEST(type != 0);
        TEST(!PyErr_Occurred());

        {{ c_type }} components[10] = {
            {% for i in range(10) %}
                {{ i }}{% if i != 9 %}, {% endif %}
            {% endfor %}
        };
        for (size_t i = 0; i < 10; i++)
        {
            PyObject *obj = api->{{ type }}Array_Create(i, components);
            TEST(obj != 0);
            TEST(!PyErr_Occurred());
            TEST(Py_TYPE(obj) == type);

            size_t length = api->{{ type }}Array_GetLength(obj);
            TEST(length == i);
            TEST(!PyErr_Occurred());

            {{ c_type }} *value_ptr = api->{{ type }}Array_GetValuePointer(obj);
            if (i == 0)
            {
                TEST(value_ptr == 0);
            }
            else
            {
                TEST(value_ptr != 0);
            }
            TEST(!PyErr_Occurred());
            for (size_t j = 0; j < i; j++)
            {
                TEST(value_ptr[j] == ({{ c_type }})j);
            }

            Py_DECREF(obj);
        }

        Py_INCREF(Py_None);
        size_t length = api->{{ type }}Array_GetLength(Py_None);
        TEST(length == 0);
        TEST(PyErr_Occurred());
        PyErr_Clear();
        {{ c_type }} *value_ptr = api->{{ type }}Array_GetValuePointer(Py_None);
        TEST(value_ptr == 0);
        TEST(PyErr_Occurred());
        PyErr_Clear();
        Py_DECREF(Py_None);

        EMathApi_Release();
        TEST(!PyErr_Occurred());

        Py_RETURN_NONE;
    }
{% endwith %}
{% endfor %}


static PyMethodDef module_methods[] = {
    {"test_EMathApi_Get", test_EMathApi_Get, METH_NOARGS, 0},
    {% for type in vector_types %}
        {"test_{{ type }}", test_{{ type }}, METH_NOARGS, 0},
        {"test_{{ type }}Array", test_{{ type }}Array, METH_NOARGS, 0},
    {% endfor %}
    {% for type in matrix_types %}
        {"test_{{ type }}", test_{{ type }}, METH_NOARGS, 0},
        {"test_{{ type }}Array", test_{{ type }}Array, METH_NOARGS, 0},
    {% endfor %}
    {% for type in quaternion_types %}
        {"test_{{ type }}", test_{{ type }}, METH_NOARGS, 0},
        {"test_{{ type }}Array", test_{{ type }}Array, METH_NOARGS, 0},
    {% endfor %}
    {% for type in pod_types %}
        {"test_{{ type }}Array", test_{{ type }}Array, METH_NOARGS, 0},
    {% endfor %}
    {0, 0, 0, 0}
};


static struct PyModuleDef module_PyModuleDef = {
    PyModuleDef_HEAD_INIT,
    "emath._test_api",
    0,
    0,
    module_methods,
    0,
    0,
    0
};


PyMODINIT_FUNC
PyInit__test_api()
{
    return PyModule_Create(&module_PyModuleDef);
}
