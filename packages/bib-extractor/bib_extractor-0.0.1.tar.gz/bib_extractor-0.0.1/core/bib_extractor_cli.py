import argparse
import logging
import os
# from system_loader import SystemLoader, SystemNotLoadException
# from core_modules import BaseABC
# import time 
# import copy
# import json
# from multiprocess import Multiproc
from bib_extractor_main import BibExtractor


def _parser():
    parser = argparse.ArgumentParser(description='Bibliographic reference processing CLI')
    parser.add_argument('--config', default='./config.json', help='Path to the config file')
    parser.add_argument("--verbose", "-v", action="store_true", help='Debug mode in logs')
    parser.add_argument("--proc_cnt", "-p", default=2, type=int, help="count of processes")
    parser.add_argument('--log', default='common_log.log', help='Name of common log file')


    subparsers = parser.add_subparsers(dest='command', required=True)

    pipeline_parser = subparsers.add_parser('pipeline', help='Run the full pipeline')
    pipeline_parser.add_argument('--texts_file', type=str, default='', help='Path to file with paths to text')
    pipeline_parser.add_argument('--out_file', type=str, default='', help='Path to output JSON file with list of dict with validated references for each input text')
    pipeline_parser.add_argument('--append_out_file', '-a', action='store_true', default=False, help='Append in existing out file. By default rewrite out file')

    extract_parser = subparsers.add_parser('extract', help='Extract references from text')
    extract_parser.add_argument('--texts_file', type=str, default='', help='Path to file with paths to text')
    extract_parser.add_argument('--out_file', type=str, default='extracted_refs.out', help='Path to output JSON file with list of founded references')
    extract_parser.add_argument('--append_out_file', '-a', action='store_true', default=False, help='Append in existing out file. By default rewrite out file')


    parse_parser = subparsers.add_parser('parse', help='Parse a reference')
    parse_parser.add_argument('--refs_file', type=str, default='', help='Path to JSON file with list of references to parse')
    parse_parser.add_argument('--parser', default=None, help='Unique name of the parser module from config')
    parse_parser.add_argument('--out_file', type=str, default='', help='Path to output JSON file with list of dict with parsed references')
    parse_parser.add_argument('--append_out_file', '-a', action='store_true', default=False, help='Append in existing out file. By default rewrite out file')

    validate_parser = subparsers.add_parser('validate', help='Validate metadata')
    validate_parser.add_argument('--refs_file', type=str, default='', help='Path to JSON file with list of references (or dict with parsed references) to validate')
    validate_parser.add_argument('--validator', default=None, help='Unique name of the validator module from config')
    validate_parser.add_argument('--out_file', type=str, default='', help='Path to output JSON file with list of dict with validated references')
    validate_parser.add_argument('--append_out_file', '-a', action='store_true', default=False, help='Append in existing out file. By default rewrite out file')

    bib_formatter_parser = subparsers.add_parser('bibformate', help='Formate bib reference')
    bib_formatter_parser.add_argument('--meta_file', type=str, default='', help='Path to JSON file with list of dict with meta of references to formate bib')
    bib_formatter_parser.add_argument('--out_dir', type=str, default='', help='Path to directory for BIB files for references')
    bib_formatter_parser.add_argument('--recreate_dir', '-r', action='store_true', default=False, help='Recreate directory if exist. By default append in existing directories')

    return parser


def process(opts):
    BE = BibExtractor(opts)
    
    if 'append_out_file' in opts and not opts.append_out_file:
        # rewrite out file
        BE.system_loader.rewrite_json(opts.out_file)

    if opts.command == 'pipeline':
        opts.logger.info(f"Pipeline mode CLI")
        texts_in_string = []
        text_paths = BE.base_class.read_file_list(opts.texts_file)
        for text_path in text_paths:
            text = BE.base_class.get_text_content_from_file(text_path)
            texts_in_string.append(text)
        result_data_gen = BE.pipeline(texts_in_string, texts_filenames=text_paths)
        for result_data in result_data_gen:
            BE.base_class.append_to_json(opts.out_file, result_data)


    elif opts.command == 'extract':
        opts.logger.info(f"Extractor mode CLI")
        texts_in_string = []
        text_paths = BE.base_class.read_file_list(opts.texts_file)
        for text_path in text_paths:
            text = BE.base_class.get_text_content_from_file(text_path)
            texts_in_string.append(text)
        bibrefs_lists_gen = BE.extract(texts_in_string)
        for index, refs_lst in enumerate(bibrefs_lists_gen):
            refs_res = {'file': text_paths[index], 'refs': refs_lst}
            opts.logger.debug(f"REFS RESULT {len(refs_res['refs'])}: {refs_res}")
            BE.base_class.append_to_json(opts.out_file, refs_res)
        opts.logger.info(f"Bib refs extracted successfully and added in file '{opts.out_file}'")

    elif opts.command == 'parse':
        opts.logger.info(f"Parse mode CLI")
        load_data = BE.base_class.load_json_from_file(opts.refs_file)
        merged_parsed_data_gen = BE.parse(load_data)
        for merged_parsed_data in merged_parsed_data_gen:
            BE.base_class.append_to_json(opts.out_file, merged_parsed_data)
        opts.logger.info(f"Parsed successfully and added in file '{opts.out_file}'")


    elif opts.command == 'validate':
        opts.logger.info(f"Validator mode CLI")
        load_data = BE.base_class.load_json_from_file(opts.refs_file)
        merged_valid_data_gen = BE.validate(load_data)
        for merged_valid_data in merged_valid_data_gen:
            BE.base_class.append_to_json(opts.out_file, merged_valid_data)
        opts.logger.info(f"Validate successfully and added in file '{opts.out_file}'")


    elif opts.command == 'bibformate':
        opts.logger.info(f"BibFormatter mode CLI")
        load_data = BE.base_class.load_json_from_file(opts.meta_file)
        bibformatter_data = BE.bibformate(load_data)
        for bibformatter_data_elem in bibformatter_data:
            # BE.base_class.append_to_json('out_bibformate_test.json', bibformatter_data_elem)
            dir_path_for_bib = BE.base_class.create_directory_for_bib_files(bibformatter_data_elem['file'], opts.out_dir, opts.recreate_dir)
            for bib_ref in bibformatter_data_elem['refs']:
                bibtex = bib_ref['bibtex']
                BE.base_class.write_bib_file(os.path.join(dir_path_for_bib, f"{bibtex['bibtex_id']}.bib"), bibtex['bibtex_string'])
                BE.base_class.logger.info(f"Bib file '{bibtex['bibtex_id']}.bib' created")

    else:
        raise RuntimeError("Unknown mode!")
    
    # общий запуск

def main():
    parser = _parser()
    parser.set_defaults(func=process)
    args = parser.parse_args()

    FORMAT = "%(asctime)s %(levelname)s [%(process)s]: %(name)s: %(classname)s: %(message)s"
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format=FORMAT,
                        filename=args.log, filemode="w")
    logger = logging.getLogger(__name__)
    logger = logging.LoggerAdapter(logger, {'classname': 'Main'})
    args.logger = logger
    
    logger.info(f"START SCRIPT")
    logger.info(f"OPTS: {args}")


    try:
        args.func(args)
    except Exception as e:
        logger.exception("failed to communicate: %s " % str(e))

    
    logger.info(f"FINISH SCRIPT")


if __name__ == '__main__':
    main()