/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {ListRenderer} from "@web/views/list/list_renderer";
import {NeokPOTRenderer} from "./renderer";

patch(ListRenderer.prototype, 'previously_opened_tasks.NeokListRenderer', NeokPOTRenderer);